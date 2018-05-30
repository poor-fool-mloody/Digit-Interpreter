from multiprocessing import Process
import csv
import operator


class TrainData:
    error = [0 for i in range(4)]  # suma wszystkich bledow dla k sasiadow
    error_table = [[0 for i in range(10)] for j in range(10)]

    def __init__(self, train_data='', test_data='', k=3, output_file='output'):
        self.train_data = train_data
        self.test_data = test_data
        self.output_file = output_file
        self.k = k

    def knn(self):

        # otwarcie pliku mnist_test.csv
        with open(self.test_data, 'r') as test_data:
            test_reader = csv.reader(test_data, delimiter=',')

            with open(self.train_data, 'r') as train_data:
                train_reader = csv.reader(train_data, delimiter=',')

                with open(self.output_file, 'w', newline='') as output_file:
                    fieldnames = ['cyfra testowana', 'cyfra sklasyfikowana dla k=1', 'k=3', 'k=5', 'k=7']
                    output_writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=',')
                    output_writer.writeheader()

                    for test_digit in test_reader:
                        tmp = []  # tymczasowa lista [ wartoscCyfryUczacej, odlegloscCyfryTestujacejOdUczacej ]
                        train_data.seek(0)

                        for train_digit in train_reader:
                            distance = self.euclideanDistance(train_digit, test_digit)
                            tmp.append([train_digit[0], distance])

                        classified = self.classify(tmp)
                        output_writer.writerow(
                            {fieldnames[0]: test_digit[0], fieldnames[1]: classified[0], fieldnames[2]: classified[1],
                             fieldnames[3]: classified[2], fieldnames[4]: classified[3]})
                        self.statistics(classified, test_digit)  # write additional statistics to anoother file

    def euclideanDistance(self, vect_1, vect_2):
        distance = 0
        for column in range(1, len(vect_1)):
            distance += (int(vect_1[column]) - int(vect_2[column])) ** 2

        return distance ** .5

    def classify(self, distances):
        classification_votes = {}
        sorted_classification_votes_table = []
        distances.sort(key=operator.itemgetter(1))

        for x in range(self.k):
            vote = distances[x][0]
            if vote in classification_votes:
                classification_votes[vote] += 1
            else:
                classification_votes[vote] = 1
            if x == 0 or x == 2 or x == 4 or x == 6:  # k od 1 do 7
                sorted_classification_votes = sorted(classification_votes.items(), key=operator.itemgetter(1),
                                                     reverse=True)
                # print(sorted_classification_votes)
                sorted_classification_votes_table.append(sorted_classification_votes[0][0])
        # print("tralalala tablica xd: ", sorted_classification_votes_table)

        return sorted_classification_votes_table

    # TODO
    ''' - rozne k check!
        - rozbieznosc 
        - ktore cyfry sie myla check!
        - wykres wartosci bledu w zaleznosci od k
        - using 4 cores
    '''

    def statistics(self, classified, test_digit):

        for x in range(len(classified)):
            if int(classified[x]) != int(test_digit[0]):
                self.error[x] += 1
                # self.error_table[int(test_digit[0])][int(classified)] += 1
                # print("pomylone ", int(test_digit[0]), int(classified))
                # for x in range(len(self.error_table)):
                #     print(self.error_table[x])
                # print("next:")
                # print(error_table[int(test_digit[0])][int(classified)])
        print("errors:", self.error)


def main():
    train_data = 'mnist_train.csv'
    test_data = 'mnist_test.csv'
    k = 7

    object1 = TrainData(train_data, test_data, k)
    object1.knn()

    # p1 = Process(target=, args=())
    # p2 = Process(target=, args=())
    # p3 = Process(target=, args=())
    # p4 = Process(target=, args=())


if __name__ == '__main__':
    main()
