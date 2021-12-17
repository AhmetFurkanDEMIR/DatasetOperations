![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white) ![](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white) ![](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)

# demir.ai Dataset Operations

With this application, you can have the empty values (nan/null) deleted or filled before giving your dataset to machine learning algorithms, you can access visual or numerical information about your dataset and have more detailed information about your attributes. 

The application is written in Python programming language, Flask framework is used in the backend, Html is used in the frontent. Pandas framework is used to navigate over the dataset, all numerical operations on the dataset were written by me and no ready-made functions were used, while the plots were created from scratch by me using the Opencv framework.

Before running the application, you can install the necessary packages for the application with the following command.
```console
pip3 install -r requirements.txt
```

You can launch the web application with the following command, and then you can use the application by going to http://localhost:5000/.
```console
python3 main.py
```

With this web application, you can delete rows or columns with empty values (nan/null) on your dataset or fill these empty values in three different ways.

* Null value (nan) operations you can do on your dataset with demir.ai Dataset Operations:

    * Column-based deletion of null data (nan/null)
    * Row-based deletion of null data (nan/null)
    * Filling in blank data by mean, median and mode
    
Again, thanks to this web application, you can reach visual or numerical results about your dataset and have detailed information about your dataset.

* Information you can learn about your dataset with demir.ai Dataset Operations:

    * Mean of columns
    * Median of columns
    * Mode of columns
    * Frequency of columns
    * Interquartile range value (IQR) of columns
    * Outliers of columns
    * Five number summary of columns
    * Box Chart of columns
    * Variance and standard deviation of columns
    

### Null value (nan/null) operations

* Column-based deletion of null data (nan/null): The number of nulls is calculated for each column, then the percentage of nulls is calculated and if this percentage is greater than the percentage the user enters, this column is deleted.

* Row-based deletion of null data (nan/null): The number of nulls is calculated for each line, and if this number of nulls is greater than the number entered by the user, this line is deleted.

* Filling in blank data by mean, median and mode:

    * Mean: The sum of the non-blank values of the columns is taken and divided by the total number of non-blank values, the average obtained is written instead of the empty values.
    
    * Median: The median is calculated according to the non-blank values in the columns, and then this median value is written instead of the empty columns.
    
    * Mode: The mode is calculated according to the non-blank values in the columns, and then this mode value is written instead of the empty columns


### Information you can learn about your dataset

* Mean of columns: The mean is calculated for each column separately and the column mean information is presented to the user.

* Median of columns: The median is calculated for each column separately and the column median information is presented to the user.

* Mode of columns: The mode is calculated for each column separately and the column mode information is presented to the user.

* Frequency of columns: Frequency is calculated for each column and the frequency information of the columns is presented to the user. In this section, frequency visualization is also done by creating a bar plot from scratch with Opencv.

* Interquartile range value (IQR) of columns: Q1 and Q3 values ​​are found for each column, then the IQR value of the columns is found with Q3-Q1 and presented to the user.

* Outliers of columns: If the data in the column is less than (Q1-IQR * 1.5) and greater than (Q3+IQR * 1.5), it is called outlier and this information is presented to the user.

* Five number summary of columns: Minimum, Q1, median, Q3 and Maximum values are calculated and presented to the user. 

* Box Chart of columns: After finding the minimum, Q1, median, Q3 and maximum values for each column, a box chart is created from scratch with Opencv and this chart is presented to the user.

* Variance and standard deviation of columns: The variance and standard deviation for each column are calculated and presented to the user.


### Application video

Link


