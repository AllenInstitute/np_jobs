from np_jobs.queues.sqlite_isilon.base import SqliteIsilonJobQueue
   
class VBNUploadQueue(SqliteIsilonJobQueue):
    
    table_name = 'vbn_upload'