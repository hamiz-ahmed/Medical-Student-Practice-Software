# Medical Students Practices Software

## Introduction

This repo provides an implementation of the Medical Students Practice Pairs. In the solution, an algorithm is implemented that assigns medical students to practices in the best way possible keeping in mind the information they have provided, including their addresses and alternate addresses. The code is completed within 48 hours. The algorithm makes use of google distance api matrix to query the distance between two particular locations.

## Algorithm
The algorithm takes as input, two csv files. The first csv file contains information provided by different students and the second contains information provided by the medical practices. The information includes their addresses as well as different information, such as whether the student has a car or does he/she have any children.

The algorithm that I have created, starts off by reading all the information of students and practices in the form of a pandas Dataframe. Once, the information is extracted, another csv file is created which is saved as `data/addresses.csv`. The file contains combinations of all possible addresses of student against practice and whether it is a bicycle or a car route. Each row of this file contains the address of the student, the address of the practice, and wehther the route to be queried should contain bike or not. For example, a sample row of the file is as follows:

```
stud_add                                |prac_add                               | is_car 
Ulrichstraße 43, 60433 Frankfurt am Main | Kantstraße 13, 60316 Frankfurt am Main | 0
```

Each row corresponds to single address of the student against the practice. If alternate addresses have been provided by the student, they are written in separate row against the practice address. All people, having cars are also queried listed down for not having it, in case, if bicycle route is shorter than car one.

In the next step, the route is queried from Google Distance Matrix with student address as the source and practice address as the destination with the mode specified as car or bicycle. The distance and duration is saved in same csv file. After this step, each row of the file looks as follows:

```
stud_add                                |prac_add                               | is_car | distance | duration
Ulrichstraße 43, 60433 Frankfurt am Main | Kantstraße 13, 60316 Frankfurt am Main | 0 | 11420 | 2207
```

Ater this, the weight for each student againt the practice is computed. The total student-pair weight is computed as follows:
1. Compute the shortest duration distance for a particular student to the pracitce. This takes in to account all his addresses and whether he has a car or not
2. Find the number of matching specialities of the student with the practice
3. Find whether the person has a child or not

A weight of 50 is assigned to the duration, a weight of 30 is assigned to number of matching specialities and a weight of 20 is assigned to person having children. Hence the total weight is computed as follows:

```python
weight = (0.2(shortest_duration) + 99(matching_specialities) + 0.8(has_child)) / 100
```
Once the weights are computed, against all possible combinations of students against practices, the best weights for each student is extracted.

## Assumptions
The algorithm is designed keeping in mind the following assumptions:
1. Each student has to be assigned to one practice.
2. Every student having the car can also have a bike.
3. The matching specialities is the most important criteria for selecting the practice.

## Challenges
There were a number of factors to consider when the algorithm had to be designed.
1. The initial help for the coding challenge was only provided for typescript. Hence, all the boilerplate code had to be written down using python conventions
2. The API quota was very limited and so was the margin for error. This had to be kept in mind while designing the algorithm and no testing queries could have been sent to the API. Hence, the response format had to be checked from the documentation and code had to be prepared before querying the API.
3. Finding a suitable technique to find the shortest travel duration keeping in mind the alternate addresses as well as whether person has a car or not was one of the major challenge. This part took a lot of thinking and time.

## Results
The final result csv file can be viewed at `data/best_pairs.csv`. The distribution that has been produced seems fair as the maximum travel duration that a person has to travel in the result is 10 minutes. However, the specialities have not been provided by all the practices and this makes the distribution biased towards the duration of the practice only. Playing with the weights doesn't yield much different results as many practices have specialities missing in them.

## Installation

The code uses Python 3.7 and can be executed by providing the Google MAPS api key in the config.json file. The requirements can be installed by:
```
pip install -r requirements.txt
```
Once the requirements are satisfied, run the following command:
```
make all
```

This will perform all the unitest, checkstyle and will run the main python file.
