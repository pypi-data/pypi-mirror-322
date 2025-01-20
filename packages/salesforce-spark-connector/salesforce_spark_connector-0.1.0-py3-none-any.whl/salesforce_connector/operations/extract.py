import re
from typing import List, Tuple, Any, Optional
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from ..utils.query_utils import (
    get_object_name, 
    get_sobject,
    parse_salesforce_datetime
)

class DataExtractor:
    def __init__(self, sf, spark, cache, logger):
        """Initialize the DataExtractor.
        
        Args:
            sf: Salesforce connection object
            spark: Spark session
            cache: Cache manager
            logger: Logger instance
        """
        self.sf = sf
        self.spark = spark
        self.cache = cache
        self.logger = logger

    def extract_data(self, query: str, partition_field: Optional[str] = None, 
                    num_partitions: int = 5) -> DataFrame:
        """Extract data from Salesforce.
        
        Args:
            query: SOQL query string
            partition_field: Field to use for partitioning (optional)
            num_partitions: Number of partitions to create (default: 5)
            
        Returns:
            DataFrame: Spark DataFrame containing the query results
        """
        try:
            if partition_field and num_partitions > 1:
                self.logger.info(f"Using parallel extraction with {num_partitions} partitions")
                return self._extract_parallel(query, partition_field, num_partitions)
            else:
                self.logger.info("Using single extraction")
                return self._extract_single(query)
        except Exception as e:
            self.logger.error(f"Data extraction failed: {str(e)}")
            raise

    def _get_field_type(self, field_info: dict) -> str:
        """Get the field type from field info."""
        field_type = field_info['type'].lower()
        
        # Map Salesforce types to our internal types
        if field_type == 'id':
            return 'id'
        elif field_type in ['currency', 'double', 'int', 'decimal', 'number']:
            return 'number'
        elif field_type in ['datetime', 'date']:
            return 'datetime'
        else:
            return 'string'

    def _create_empty_schema(self, query: str) -> StructType:
        """Create an empty schema based on the query fields."""
        import re
        field_match = re.search(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE)
        if not field_match:
            raise ValueError("Could not parse fields from query")
            
        fields = [f.strip() for f in field_match.group(1).split(',')]
        schema_fields = []
        
        for field in fields:
            field = field.split(' AS ')[-1].strip()
            if field.lower() in ['amount', 'revenue', 'price']:
                schema_fields.append(StructField(field, DoubleType(), True))
            elif 'date' in field.lower():
                schema_fields.append(StructField(field, TimestampType(), True))
            else:
                schema_fields.append(StructField(field, StringType(), True))
                
        return StructType(schema_fields)

    def _create_partitioned_query(self, base_query: str, partition_field: str,
                                range_start: Any, range_end: Any, field_type: str) -> str:
        """Create a query for a specific partition range."""
        if "WHERE" in base_query.upper():
            connector = "AND"
        else:
            connector = "WHERE"

        if field_type == 'id':
            # For ID fields, use IN operator with the list of IDs
            id_list = range_start if isinstance(range_start, list) else [range_start]
            formatted_ids = "'" + "','".join(id_list) + "'"
            return f"{base_query} {connector} {partition_field} IN ({formatted_ids})"
        elif field_type == 'datetime':
            return f"{base_query} {connector} {partition_field} >= {range_start} AND {partition_field} < {range_end}"
        elif field_type == 'number':
            # Remove quotes for number fields and ensure they're treated as numbers
            start_val = float(range_start)
            end_val = float(range_end)
            return f"{base_query} {connector} {partition_field} >= {start_val} AND {partition_field} < {end_val}"
        else:  # string type
            return f"{base_query} {connector} {partition_field} >= '{range_start}' AND {partition_field} < '{range_end}'"

    def create_partition_ranges(self, field_type: str, min_val: Any, max_val: Any, 
                              num_partitions: int, base_query: str = None) -> List[Tuple[str, str]]:
        """Create partition ranges based on field type."""
        if field_type == 'id':
            if not base_query:
                return []
            
            # Extract the object name and WHERE clause from the original query
            object_match = re.search(r'FROM\s+(\w+)', base_query, re.IGNORECASE)
            where_clause = ""
            if "WHERE" in base_query.upper():
                where_clause = base_query[base_query.upper().index("WHERE"):]
            
            if not object_match:
                return []
            
            object_name = object_match.group(1)
            
            # Get a batch of IDs that match the where clause
            count_query = f"SELECT COUNT(Id) total FROM {object_name} {where_clause}"
            result = self.sf.query(count_query)
            total_records = result['records'][0]['total']
            
            if total_records == 0:
                return []
            
            # Calculate batch size based on total records and desired partitions
            batch_size = max(1, min(2000, total_records // num_partitions))
            
            # Get IDs in batches
            id_query = f"SELECT Id FROM {object_name} {where_clause} ORDER BY Id"
            result = self.sf.query(id_query)
            
            ranges = []
            current_batch = []
            
            while True:
                for record in result['records']:
                    current_batch.append(record['Id'])
                    if len(current_batch) >= batch_size:
                        ranges.append((current_batch[:], ''))
                        current_batch = []
                    
                if result.get('done', True):
                    break
                result = self.sf.query_more(result['nextRecordsUrl'])
            
            # Add any remaining IDs as the final batch
            if current_batch:
                ranges.append((current_batch, ''))
            
            return ranges

        elif field_type == 'datetime':
            if not min_val or not max_val:
                return []
                
            min_date = parse_salesforce_datetime(min_val)
            max_date = parse_salesforce_datetime(max_val)
            delta = (max_date - min_date) / num_partitions
            
            ranges = []
            for i in range(num_partitions):
                start_date = min_date + (delta * i)
                end_date = min_date + (delta * (i + 1))
                start_str = start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                end_str = end_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                ranges.append((start_str, end_str))
            return ranges
            
        elif field_type == 'number':
            if not min_val or not max_val:
                return []
                
            min_num = float(min_val)
            max_num = float(max_val)
            step = (max_num - min_num) / num_partitions
            return [(str(min_num + (step * i)), str(min_num + (step * (i + 1))))
                   for i in range(num_partitions)]
        
        else:  # string type
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            step = max(1, len(chars) // num_partitions)
            ranges = []
            for i in range(0, len(chars), step):
                start_char = chars[i]
                end_char = chars[min(i + step, len(chars) - 1)]
                ranges.append((start_char, end_char))
            return ranges

    def _extract_parallel(self, base_query: str, partition_field: str, 
                         num_partitions: int) -> DataFrame:
        """Extract data in parallel using partitioning."""
        try:
            # Get field type
            object_name = get_object_name(base_query)
            sobject = get_sobject(self.sf, object_name)
            field_info = next(
                (f for f in sobject.describe()['fields'] 
                 if f['name'].lower() == partition_field.lower()),
                None
            )
            
            if not field_info:
                raise ValueError(f"Field {partition_field} not found in {object_name}")
                
            field_type = self._get_field_type(field_info)
            self.logger.debug(f"Field {partition_field} detected as type: {field_type}")
            
            # Create ranges based on field type
            if field_type == 'id':
                ranges = self.create_partition_ranges('id', None, None, num_partitions, base_query)
            else:
                # Get min and max values for non-ID fields
                min_max_query = f"SELECT MIN({partition_field}), MAX({partition_field}) FROM {object_name}"
                if "WHERE" in base_query.upper():
                    where_clause = base_query[base_query.upper().index("WHERE"):]
                    min_max_query += f" {where_clause}"
                    
                result = self.sf.query(min_max_query)
                if not result['records']:
                    return self.spark.createDataFrame([], self._create_empty_schema(base_query))
                    
                min_val = result['records'][0][f'expr0']
                max_val = result['records'][0][f'expr1']
                ranges = self.create_partition_ranges(field_type, min_val, max_val, num_partitions)
                
            # Execute parallel queries
            results = []
            for start_range, end_range in ranges:
                partitioned_query = self._create_partitioned_query(
                    base_query, partition_field, start_range, end_range, field_type
                )
                self.logger.debug(f"Executing partition query: {partitioned_query}")
                partition_result = self.sf.query(partitioned_query)
                if partition_result['records']:
                    results.extend(partition_result['records'])
                    
            # Process results
            if not results:
                return self.spark.createDataFrame([], self._create_empty_schema(base_query))
                
            # Clean and return results
            cleaned_results = []
            for record in results:
                record_dict = dict(record)
                record_dict.pop('attributes', None)
                cleaned_results.append(record_dict)
                
            return self.spark.createDataFrame(cleaned_results)
            
        except Exception as e:
            self.logger.error(f"Parallel extraction failed: {str(e)}")
            self.logger.info("Falling back to single extraction")
            return self._extract_single(base_query)

    def _extract_single(self, query: str) -> DataFrame:
        """Extract data using a single query."""
        try:
            result = self.sf.query(query)
            if not result['records']:
                return self.spark.createDataFrame([], self._create_empty_schema(query))
                
            # Clean the results by removing the 'attributes' field
            cleaned_records = []
            for record in result['records']:
                record_dict = dict(record)
                record_dict.pop('attributes', None)
                cleaned_records.append(record_dict)
                
            return self.spark.createDataFrame(cleaned_records)
            
        except Exception as e:
            raise RuntimeError(f"Failed to execute query: {str(e)}") 