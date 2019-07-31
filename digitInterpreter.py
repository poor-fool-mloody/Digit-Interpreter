import csv
import operator
import matplotlib.pyplot as plt  # library for plotting charts


def knn(train_data, test_data, k):
    output_file_classification = 'classification.csv'  # output file with classified digits for k=1..k neighbours respectively
    output_file_errors = 'errors.csv'  # total amount of bad predictions for k=1..k neighbours respectively
    output_file_errors2 = 'errors.csv'  # total amount of bad predictions for k=1..k neighbours respectively

    error = [0 for x in range(
        k)]  # this list hold total amount of bad predictions for k=1..k neighbours respectively

    with open(test_data, 'r') as test_data:  # read test dataset
        test_reader = csv.reader(test_data, delimiter=',')

        with open(train_data, 'r') as train_data:  # read train dataset
            train_reader = csv.reader(train_data, delimiter=',')

            with open(output_file_classification, 'w',
                      newline='') as output_file_classification:  # open output file for writing classified info for k=1..k neighbours
                fieldnames = ['test digit', 'digit clasified for k=1', 'k=2', 'k=3', 'k=4', 'k=5', 'k=6',
                              'k=7']  # define column names
                output_writer = csv.DictWriter(output_file_classification, fieldnames=fieldnames, delimiter=',')
                output_writer.writeheader()

                with open(output_file_errors, 'w',
                          newline='') as output_file_errors:  # open output file for writing total amount of bad predictions for k=1..k neighbours respectively
                    fieldnames2 = ['k', 'number of errors']  # define column names
                    output_writer2 = csv.DictWriter(output_file_errors, fieldnames=fieldnames2, delimiter=',')
                    output_writer2.writeheader()

                    for test_digit in test_reader:  # loop over every record from test dataset
                        tmp = []  # temporary list containing Euclidean distance between test digit vector and train digit vector
                        train_data.seek(
                            0)  # set file reading pointer to the beginning of the file

                        for train_digit in train_reader:  # loop over every record from train dataset
                            distance = euclidean_distance(train_digit,
                                                          test_digit)  # list that contains test digit value and its distance to train digit
                            tmp.append([train_digit[0], distance])  # append new distance to tmp list

                        classified = classify(tmp,
                                              k)  # list that contains classification results for k=1..k neighbours respectively
                        output_writer.writerow(  # write classified digits into classified.csv
                            {fieldnames[0]: test_digit[0], fieldnames[1]: classified[0], fieldnames[2]: classified[1],
                             fieldnames[3]: classified[2], fieldnames[4]: classified[3], fieldnames[5]: classified[2],
                             fieldnames[6]: classified[3], fieldnames[7]: classified[3]})

                        errors(classified, test_digit, error)

                    for x in range(k):  # write classification errors to errors.csv for k=1..k neighbours respectively
                        output_writer2.writerow({fieldnames2[0]: x + 1, fieldnames2[1]: error[x]})

    with open(output_file_errors2, 'r') as output_file_errors:  # open file containing classification errors for reading
        output_reader = csv.reader(output_file_errors, delimiter=',')
        x = []
        y = []
        output_file_errors.seek(0)
        next(output_reader)
        for row in output_reader:
            x.append(int(row[0]))
            y.append(int(row[1]))

        plt.plot(x, y, 'ro')
        plt.title('Error chart')
        plt.xlabel('number of neighbours')
        plt.ylabel('total amount of bad predictions')
        plt.show()


def euclidean_distance(vect_1, vect_2):  # utility function computing Euclidean distance between two given vectors
    distance = 0
    for column in range(1, len(vect_1)):
        distance += (int(vect_1[column]) - int(vect_2[column])) ** 2
    return distance ** .5


def classify(distances, k):  # function for predicting what class digit belongs
    classification_digits = {}  # dictionary that holds number of same digit occurence for k=1..k shortest distances
    sorted_classification_digits_table = []
    distances.sort(key=operator.itemgetter(
        1))

    for x in range(k):
        digit = distances[x][0]
        if digit in classification_digits:  # if digit appeared in x shortest distance then increase appearence counter of this digit
            classification_digits[digit] += 1
        else:  # set digit occurrence to 1
            classification_digits[digit] = 1
        sorted_classification_digits = sorted(classification_digits.items(), key=operator.itemgetter(1),
                                              reverse=True)  # sort dictionary descending
        sorted_classification_digits_table.append(sorted_classification_digits[0][
                                                      0])

    return sorted_classification_digits_table


def errors(classified,
           test_digit,
           error):  # function that increase amount of bad predictions for k=1..k neighbours respectively
    for x in range(len(classified)):
        if int(classified[x]) != int(test_digit[0]):
            error[x] += 1
    print("errors:", error)


def main():
    train_data = 'mnist_train.csv'  # train dataset
    test_data = 'mnist_test.csv'  # test dataset
    k = 7  # number of neighbours

    knn(train_data, test_data,
        k)  # run prediction


if __name__ == '__main__':
    main()
