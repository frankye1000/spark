df = spark.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://10.120.37.108/project.comments").load()
val df1=df.select($"person_id",$"politician_id")
val rdd = df1.rdd
val rdd1 = rdd.map( x => (x(0),x(1) ))
case class transform( politician_id:String,person_id:String )
val rdd1 = rdd.map(x => ( x(0).asInstanceOf[String] , x(1).asInstanceOf[String] ))
val rdd2 = rdd1.map(  x => ( x._1 , Set(x._2 ) )      )
val rdd3 = rdd2.reduceByKey((x,y) => x ++ y)
val rdd4 = rdd3.filter(x => x._2.size > 1)
val rdd5 = rdd4.map(x=>(x._2.toList.sorted ))
val rdd6 = rdd5.map(x => x.combinations(2).toList)








