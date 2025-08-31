import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import col, substring, count

# Glueジョブ引数
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# ==============================
# 1. データソースをGlue Catalogから読み込み
# ==============================
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="mydefault",      # Glue Catalogのデータベース名
    table_name="my-athenaresults"  # Glue Catalogのテーブル名
)

# DynamicFrame → DataFrame に変換
df = datasource.toDF()

# ==============================
# 2. 集計処理 (IDの先頭文字ごとの件数)
# ==============================
aggregated = df.groupBy(substring(col("no.string"), 1, 1).alias("first_char")) \
               .agg(count("*").alias("cnt"))

# ==============================
# 3. DataFrame → DynamicFrame に戻す
# ==============================
aggregated_dynamic = DynamicFrame.fromDF(aggregated, glueContext, "aggregated_dynamic")

# ==============================
# 4. S3にParquet形式で書き出す
# ==============================
output_path = "s3://galaxy-sg-001/aggregated-data/"  # 集計結果を保存するS3パス
glueContext.write_dynamic_frame.from_options(
    frame=aggregated_dynamic,
    connection_type="s3",
    connection_options={"path": output_path},
    format="parquet"
)

# ==============================
# 5. ジョブ終了
# ==============================
job.commit()
