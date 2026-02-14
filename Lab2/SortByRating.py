from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime

class SortByRating(MRJob):

    def configure_args(self):
        super(SortByRating, self).configure_args()

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_format_output)
        ]

    def mapper_get_ratings(self, _, line):
       
        parts = line.split('\t')
        if len(parts) >= 3:
            userID = parts[0]
            movieID = parts[1]
            rating = parts[2]
            try:
                yield float(rating), (userID, movieID)
            except ValueError:
                pass

    def reducer_format_output(self, rating, values):
        for userID, movieID in values:
            yield rating, [userID, movieID]

    def jobconf(self):
       # sort keys in descending order
        return {
            'mapreduce.job.output.key.comparator.class': 'org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator',
            'mapreduce.partition.keycomparator.options': '-nr',
        }

if __name__ == '__main__':
    SortByRating.run()
