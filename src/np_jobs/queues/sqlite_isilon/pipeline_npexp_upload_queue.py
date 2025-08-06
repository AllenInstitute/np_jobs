from np_jobs.queues.sqlite_isilon.base import SqliteIsilonJobQueue
   
class PipelineNpexpUploadQueue(SqliteIsilonJobQueue):
    
    table_name = 'npexp_upload'
    column_definitions = dict(
        **SqliteIsilonJobQueue.column_definitions,
        probes='TEXT NOT NULL DEFAULT ABCDEF',
    )