#!/bin/bash

JARS_DIR="spark-jars"
mkdir -p $JARS_DIR

# Lista de JARs para download
declare -A jars=(
    ["delta-core_2.12-2.2.0.jar"]="https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.2.0/delta-core_2.12-2.2.0.jar"
    ["delta-storage-2.2.0.jar"]="https://repo1.maven.org/maven2/io/delta/delta-storage/2.2.0/delta-storage-2.2.0.jar"
    ["aws-java-sdk-bundle-1.12.431.jar"]="https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.431/aws-java-sdk-bundle-1.12.431.jar"
    ["hadoop-common-3.3.4.jar"]="https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar"
    ["hadoop-aws-3.3.4.jar"]="https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar"
)

for jar in "${!jars[@]}"; do
    if [ ! -f "$JARS_DIR/$jar" ]; then
        echo "Downloading $jar..."
        curl -L "${jars[$jar]}" -o "$JARS_DIR/$jar"
    else
        echo "$jar already exists"
    fi
done