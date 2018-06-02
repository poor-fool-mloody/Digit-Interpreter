from multiprocessing import Process
import csv
import operator

error = [0 for i in range(7)]  # lista w której przechowywane są całkowite ilości popełnionych będów klasyfikacyjnych dla k=1..k sąsiadów


# error_table = [[0 for i in range(10)] for j in range(10)]


def knn(train_data, test_data, k):
    output_file_classification = 'classification.csv' # zestaw danych sklasyfikowanych dla k=1..k
    output_file_errors = 'errors.csv' # całkowita ilość popełnionych będów klasyfikacyjnych dla k=1..k

    with open(test_data, 'r') as test_data:  #otwarcie pliku z zestawem danych testujących
        test_reader = csv.reader(test_data, delimiter=',')

        with open(train_data, 'r') as train_data:  #otwarcie pliku z zestawem danych uczących
            train_reader = csv.reader(train_data, delimiter=',')

            with open(output_file_classification, 'w', newline='') as output_file_classification: # otwarcie pliku wyjściowego zawierającego zestaw danych sklasyfikowanych dla k=1..k
                fieldnames = ['test digit', 'digit clasified for k=1', 'k=2', 'k=3', 'k=4', 'k=5', 'k=6', 'k=7'] # ustalenie nazw kolumn w pliku classification.csv
                output_writer = csv.DictWriter(output_file_classification, fieldnames=fieldnames, delimiter=',')
                output_writer.writeheader()

                with open(output_file_errors, 'w', newline='') as output_file_errors: # otwarcie pliku wyjściowego zawierającego całkowitą iloś popełnionych będów klasyfikacyjnych dla k=1..k sąsiadów
                    fieldnames2 = ['number of errors for k=1', 'k=2', 'k=3', 'k=4', 'k=5', 'k=6', 'k=7'] # ustalenie nazw kolumn w pliku errors.csv
                    output_writer2 = csv.DictWriter(output_file_errors, fieldnames=fieldnames2, delimiter=',')
                    output_writer2.writeheader()

                    for test_digit in test_reader: # pętla sczytująca każdą cyfrę testującą z zestawu cyfr testujących
                        tmp = []  # tymczasowa lista przechowująca euklidesowe odległości pomiędzy wektorem cyfry testującej od uczącej
                        train_data.seek(0) # ustawienie wskaźnika aktualnego czytania danych uczącyhc z pliku na początek

                        for train_digit in train_reader: # pętla sczytująca każdą cyfrę uczącą z zestawu cyfr uczących
                            distance = euclidean_distance(train_digit, test_digit) # lista przechowująca wartość odległości pomiędzy wektorem cyfry testującej od cyfry uczącej
                            tmp.append([train_digit[0], distance]) # poszerzenie listy o nową odległość

                        classified = classify(tmp, k) # lista przechowująca rezultat klasyfikacji dla k=1..k sąsiadów
                        output_writer.writerow( # wypisywanie sklasyfikowanych cyfr do pliku classified.csv
                            {fieldnames[0]: test_digit[0], fieldnames[1]: classified[0], fieldnames[2]: classified[1],
                             fieldnames[3]: classified[2], fieldnames[4]: classified[3], fieldnames[5]: classified[2],
                             fieldnames[6]: classified[3], fieldnames[7]: classified[3]})

                        errors(classified, test_digit)

                    output_writer2.writerow( # wypisywanie błędów klasyfikacyjnych dla k=1..k sąsiadów do pliku errors.csv
                        {fieldnames2[0]: error[0], fieldnames2[1]: error[1], fieldnames2[2]: error[2],
                         fieldnames2[3]: error[3], fieldnames2[4]: error[4], fieldnames2[5]: error[5],
                         fieldnames2[6]: error[6]})


def euclidean_distance(vect_1, vect_2): # funkcja obliczająca odległość Euklidesową pomiędzy dwoma zadanymi wektorami
    distance = 0
    for column in range(1, len(vect_1)):
        distance += (int(vect_1[column]) - int(vect_2[column])) ** 2
    return distance ** .5


def classify(distances, k): # funkcja klasyfikująca cyfrę
    classification_votes = {} # słownik przechowujący ilość wystąpień takiej samej sklasyfikowanej cyfry dla k=1..k najkrótszych odległości
    sorted_classification_votes_table = []  # is a retured list that contain classified digit for k =1, k =2,.., k = 7
    distances.sort(key=operator.itemgetter(1))

    for x in range(k):
        vote = distances[x][0]
        if vote in classification_votes:  # if
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
        - procentage value of errors
    '''


def errors(classified, test_digit): # funkcja zwiększająca licznik błędów dla k=1..k sąsiadów jeśli sklasyfikowana cyfra różni się od rzeczywistej cyfry
    for x in range(len(classified)):
        if int(classified[x]) != int(test_digit[0]):
            error[x] += 1
    print("errors:", error)


def main():
    train_data = 'mnist_train_train.csv'  # zestaw danych uczących
    test_data = 'mnist_test3.csv'  # zestaw danych testujących
    k = 7  # liczba sąsiadów

    knn(train_data, test_data, k)  # knn - funkcja klasyfikująca algorytmem k najbliższych sąsiadów zadane cyfry arabskie z zestawu testujących danych MNIST na podstawie uczącego zestawu danych MNIST.
    #  Tworzy 2 pliki: classification.csv oraz errors.csv. classification.csv zawiera zestaw cyfr oraz odpowiadające im te cyfry sklasyfikowane przez algorytm dla k=1..k sąsiadów. errors.csv zawiera całkowitą liczbę popełnionych błędów klasyfikacji dla k=1..k sąsiadów.

    # p2 = Process(target=, args=())
    # p3 = Process(target=, args=())
    # p4 = Process(target=, args=())


if __name__ == '__main__':
    main()
