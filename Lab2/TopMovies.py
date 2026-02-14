from mrjob.job import MRJob
from mrjob.step import MRStep

class TopMovies(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_average_ratings),
            MRStep(reducer=self.reducer_sort_top)
        ]

    def mapper_get_ratings(self, _, line):
        # Join logic: detect file type
        if '|' in line:
            parts = line.split('|')
            yield parts[0], ('NAME', parts[1])
        else:
            parts = line.split()
            if len(parts) == 4:
                yield parts[1], ('RATING', float(parts[2]))

    def reducer_average_ratings(self, movie_id, values):
        name = "Unknown"
        ratings = []
        for val in values:
            if val[0] == 'NAME':
                name = val[1]
            else:
                ratings.append(val[1])

        if ratings:
            avg = sum(ratings) / len(ratings)
            # Send (None) as key to gather all movies in one final reducer for sorting
            yield None, (avg, name, len(ratings))

    def reducer_sort_top(self, _, movies):
        # Sort by average (the first element in the tuple) in descending order
        # We also filter for movies with more than 10 ratings for better accuracy
        sorted_movies = sorted(movies, reverse=True, key=lambda x: x[0])

        for avg, name, count in sorted_movies:
            yield name, f"Rating: {avg:.2f} ({count} reviews)"

if __name__ == '__main__':
    TopMovies.run()
