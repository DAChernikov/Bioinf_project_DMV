for file in *1.fq.gz
do 
fastp -i $file -I ${file%1.fq.gz}2.fq.gz -o ${file%.fq.gz}_trimmed.fq.gz -O ${file%1.fq.gz}2_trimmed.fq.gz
done 


for file in *1_trimmed.fq.gz
do bowtie2 -p 4 -1 $file -2 ${file%1_trimmed.fq.gz}2_trimmed.fq.gz -x t5.bowtie2_index -S ${file%_1_trimmed.fq.gz}.sam
done


for file in *.sam
do 
samtools view -bS $file > ${file%sam}bam
samtools sort ${file%.sam}.bam ${file%.sam}_sorted.bam | samtools index ${file%.sam}_sorted.bam
done


for file in *_sorted.bam
do 
samtools depth *_sorted.bam | awk '{print $1 "\t" $2 "\t" $3}' > coverage_ ${file%_sorted.bam}.txt
done
