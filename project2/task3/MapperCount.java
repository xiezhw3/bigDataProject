package com.aamend.hadoop.mapreduce.designpattern.counter;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;
import java.util.UUID;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Counter;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import com.aamend.hadoop.mapreduce.designpattern.job.MRDPUtils;

public class MapperCount {

	public static class MapperCountDriver {

		public static void main(String[] args) throws Exception {

			Configuration conf = new Configuration();

			String output = null;
			String input = null;

			// Create Hadoop Job
			String jobName = "CounterByState_" + UUID.randomUUID();
			jobName = jobName.toUpperCase();
			Job job = new Job(conf, jobName);

			// Where to find the MR algo.
			job.setJarByClass(CountNumUsersByStateMapper.class);
			job.setMapperClass(CountNumUsersByStateMapper.class);

			// Set up input / output directories
			// Output directory must be set but will contain empty files
			Path outputPath = new Path(output + "/" + jobName);
			Path inputPath = new Path(input);
			FileInputFormat.setInputPaths(job, inputPath);
			FileOutputFormat.setOutputPath(job, outputPath);

			System.out.println("*****************************");
			System.out.println("JobName : \t" + jobName);
			System.out.println("Output Path : \t" + output + "/" + jobName);
			System.out.println("Input Path : \t" + input);
			System.out.println("*****************************");

			// keep a synchronous Hadoop call
			int code = job.waitForCompletion(true) ? 0 : 1;
			if (code == 0) {
				// Job successfully processed, retrieve counters
				for (Counter counter : job.getCounters().getGroup(
						CountNumUsersByStateMapper.SORE_GROUP)) {
					System.out.println(counter.getDisplayName() + "\t"
							+ counter.getValue());
				}
			}

			// Clean up empty output directory
			FileSystem.get(conf).delete(outputPath, true);
			System.exit(code);

		}

	}

	public class CountNumUsersByStateMapper extends
			Mapper<Object, Text, Text, DoubleWritable>{

		public static final String SORE_GROUP = "StoreType";
		public static final String STORELASVEGAS = "Las Vegas";
		public static final String STOREARLINGTON = "Arlington";
		private static LasvegasTotalScale = 0.0;
		private static ArlingtonTotalScale = 0.0;
		
		public void map(Object key, Text value, Context context)
	  			throws IOException, InterruptedException {
	  		StringTokenizer itr = new StringTokenizer(value.toString(), "\n", false);
	  		while (itr.hasMoreTokens()) {
				String str = itr.nextToken();
	  			String number[] = str.split("\t");
	  			if (number.size() != 6)
	  				continue;

	  			if (number[2] == STORELASVEGAS) {
	  				LasvegasTotalScale += Double.parseDouble(number[4]);
	  				context.getCounter(STATE_COUNTER_GROUP, STORELASVEGAS).increment(1);
	  			} else if (number[2] == STOREARLINGTON){
	  				ArlingtonTotalScale += Double.parseDouble(number[4]);
					context.getCounter(STATE_COUNTER_GROUP, STOREARLINGTON).increment(1);
	  			}
	  		}
	  		context.write(STORELASVEGAS, LasvegasTotalScale);
	  		context.write(STOREARLINGTON, ArlingtonTotalScale);
	  	}
	}
}
