from np_jobs.queues.sqlite_isilon.base import SqliteIsilonJobQueue
   
class VBNExtractionQueue(SqliteIsilonJobQueue):
    
    table_name = 'vbn_extraction'