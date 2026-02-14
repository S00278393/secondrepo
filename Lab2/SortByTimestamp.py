from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime

class SortByTimestamp(MRJob):

    def configure_args(self):
        super(SortByTimestamp, self).configure_args()

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_timestamp,
                   reducer=self.reducer_format_output)
        ]

    def mapper_get_timestamp(self, _, line):

        parts = line.split()
        if len(parts) >= 4:
            # userID, movieID, rating, timestamp = line.split()[:4]
            (userID, movieID, rating, timestamp) = line.split('\t')
            try:
                yield int(timestamp), (userID, movieID, rating)
            except ValueError:
                pass

    def reducer_format_output(self, ts, values):
        readable_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        for userID, movieID, rating in values:
            yield readable_time, [userID, movieID, rating]

if __name__ == '__main__':
    SortByTimestamp.run()
