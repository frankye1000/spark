from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", "mongodb://10.120.37.108/project.reactions") \
    .config("spark.mongodb.output.uri", "mongodb://10.120.37.108/fb_cleaned.pair_reactions") \
    .getOrCreate()

df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://10.120.37.108/project.reactions").load()
rdd = df.rdd
temp1 = rdd.map(lambda x: (x.person_id, x.post_id.split("_")[0] ))
temp2 = temp1.groupByKey()
temp3 = temp2.map(lambda x: set(list(x[1])))
temp4 = temp3.map(lambda x: sorted(x))
temp5 = temp4.filter(lambda x: len(x) >1 )



from itertools import combinations


temp6 = temp5.flatMap(lambda x: list(combinations(x, 2)))
temp7 = temp6.map(lambda x: (x,1))
temp8 = temp7.reduceByKey(lambda x,y : x+y )
temp9 = temp8.sortBy(lambda x : x[1],False)
temp10 = temp9.map(lambda x : ([ x[0][0] , x[0][1] ] , x[1] ) )
df2 = spark.createDataFrame(temp10, ["pair","numbers"])
df2.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("database","fb_cleaned").option("collection", "pair_reactions").save()