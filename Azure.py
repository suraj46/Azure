# Databricks notebook source
# DBTITLE 1,SAS Token


#?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2023-09-20T22:19:57Z&st=2023-09-20T14:19:57Z&sip=192.168.0.108&spr=https&sig=teZCme4v05nyR%2BcBTmTqQx9Tq8Gv0DqzURzb5upUvrM%3D



# COMMAND ----------

# DBTITLE 1,Load Blob
spark.conf.set(f"fs.azure.sas.projectfile.azurestorage22.blob.core.windows.net",'?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2023-09-28T20:49:19Z&st=2023-09-20T12:49:19Z&spr=https&sig=0haobw3xJIeR35%2FNRHT0wCOaqbU7nAhgA0wqhH9r5KU%3D')

# COMMAND ----------

dbutils.fs.ls('wasbs://projectfile@azurestorage22.blob.core.windows.net')

# COMMAND ----------

data1 = spark.read.csv("wasbs://projectfile@azurestorage22.blob.core.windows.net/Dataset1.csv",header=True,inferSchema=True)
data2 = spark.read.csv("wasbs://projectfile@azurestorage22.blob.core.windows.net/Dataset2.csv",header=True,inferSchema=True)


# COMMAND ----------

#data1.show()
#data2.show()

# COMMAND ----------

#data1.write.mode("overwrite").format("csv").save("wasbs://projectfile@azurestorage22.blob.core.windows.net/newDataset1.csv")
data2.write.mode("overwrite").format("csv").save("wasbs://projectfile@azurestorage22.blob.core.windows.net/newDataset2.csv")

# COMMAND ----------

# DBTITLE 1,Trasnform
from pyspark.sql.functions import col, expr

d1 = data1.filter((data1.Likes>=300) & (data1.Views>=8900000))
#d1.show()
d2 = data2.filter((data2.Likes>=300) & (data2.Views>=8900000))
#d2.show()

# COMMAND ----------

from pyspark.sql import functions as F

filter1 = d1.groupBy("VideoTitle").agg(
    F.max("Views").alias("MaxViews"),
    F.max("Likes").alias("MaxLikes"),
    F.first("VideoTitle").alias("TopVideoTitle")
 )


filter2 = d2.groupBy("VideoTitle").agg(
    F.max("Views").alias("MaxViews"),
    F.max("Likes").alias("MaxLikes"),
    F.first("VideoTitle").alias("TopVideoTitle")
 )

filter1.show()

filter2.show()





# COMMAND ----------

filter1.write.mode("overwrite").format("csv").option("header","True").save("wasbs://projectfile@azurestorage22.blob.core.windows.net/filter1")

filter2.write.mode("overwrite").format("csv").option("header","True").save("wasbs://projectfile@azurestorage22.blob.core.windows.net/filter2")





# COMMAND ----------


'''
from datetime import datetime
import pyspark.sql.functions as F
import time

# Get the current timestamp
current_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Define the dynamic output directory
output_directory = f"wasbs://projectfile@azurestorage22.blob.core.windows.net/finaldata/{current_timestamp}/"

# Append 'filter1' DataFrame to the dynamic output directory with a timestamped file name
output_path1 = output_directory + f"filterdata1_{current_timestamp}.csv"
filter1.write.mode("append").format("csv").save(output_path1)
filter2.write.mode("append").format("csv").save(output_path1)
'''


# COMMAND ----------


