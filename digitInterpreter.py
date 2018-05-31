from multiprocessing import Process
import csv
import operator

error = [0 for i in range(7)]  # total errors depending on k
# error_table = [[0 for i in range(10)] for j in range(10)]


def knn(train_data, test_data, k):
    output_file_classification = 'classification.csv'
    output_file_errors = 'errors.csv'

    # otwarcie pliku mnist_test.csv
    with open(test_data, 'r') as test_data:
        test_reader = csv.reader(test_data, delimiter=',')

        with open(train_data, 'r') as train_data:
            train_reader = csv.reader(train_data, delimiter=',')

            with open(output_file_classification, 'w', newline='') as output_file_classification:
                fieldnames = ['test digit', 'digit clasified for k=1', 'k=2', 'k=3', 'k=4', 'k=5', 'k=6', 'k=7']
                output_writer = csv.DictWriter(output_file_classification, fieldnames=fieldnames, delimiter=',')
                output_writer.writeheader()

                with open(output_file_errors, 'w', newline='') as output_file_errors:
                    fieldnames2 = ['number of errors for k=1', 'k=2', 'k=3', 'k=4', 'k=5', 'k=6', 'k=7']
                    output_writer2 = csv.DictWriter(output_file_errors, fieldnames=fieldnames2, delimiter=',')
                    output_writer2.writeheader()

                    for test_digit in test_reader:
                        tmp = []  # temporary list to specify shortest distances between vectors
                        train_data.seek(0)

                        for train_digit in train_reader:
                            distance = euclidean_distance(train_digit, test_digit)
                            tmp.append([train_digit[0], distance])

                        classified = classify(tmp, k)
                        output_writer.writerow(
                            {fieldnames[0]: test_digit[0], fieldnames[1]: classified[0], fieldnames[2]: classified[1],
                             fieldnames[3]: classified[2], fieldnames[4]: classified[3], fieldnames[5]: classified[2],
                             fieldnames[6]: classified[3], fieldnames[7]: classified[3]})

                        statistics(classified, test_digit)  # write additional statistics to another file

    output_writer2.writerow(
        {fieldnames2[0]: error[0], fieldnames2[1]: error[1], fieldnames2[2]: error[2],
         fieldnames2[3]: error[3], fieldnames2[4]: error[4], fieldnames2[5]: error[5],
         fieldnames2[6]: error[6]})


def euclidean_distance(vect_1, vect_2):
    distance = 0
    for column in range(1, len(vect_1)):
        distance += (int(vect_1[column]) - int(vect_2[column])) ** 2

    return distance ** .5


def classify(distances, k):
    classification_votes = {}
    sorted_classification_votes_table = [] # is a retured list that contain classified digit for k =1, k =2,.., k = 7
    distances.sort(key=operator.itemgetter(1))

    for x in range(k):
        vote = distances[x][0]
        if vote in classification_votes: # if
            classification_votes[vote] += 1
        else:
            classification_votes[vote] = 1
        sorted_classification_votes = sorted(classification_votes.items(), key=operator.itemgetter(1),
                                             reverse=True)
        # print(sorted_classification_votes)
        sorted_classification_votes_table.append(sorted_classification_votes[0][0])

    print(sorted_classification_votes_table)
    return sorted_classification_votes_table

    # TODO
    '''
        - rozbieznosc 
        - plot errors  depending on k
        - using 4 cores
    '''


def statistics(classified, test_digit):
    for x in range(len(classified)):
        if int(classified[x]) != int(test_digit[0]):
            error[x] += 1
            # error_table[int(test_digit[0])][int(classified)] += 1
            # print("pomylone ", int(test_digit[0]), int(classified))
            # for x in range(len(error_table)):
            #     print(error_table[x])
            # print("next:")
            # print(error_table[int(test_digit[0])][int(classified)])
    print("errors:", error)


def main():
    train_data = 'mnist_train_train.csv'
    test_data = 'mnist_test.csv'
    k = 7

    knn(train_data, test_data, k)

    # p1 = Process(target=, args=())
    # p2 = Process(target=, args=())
    # p3 = Process(target=, args=())
    # p4 = Process(target=, args=())


if __name__ == '__main__':
    main()
