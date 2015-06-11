import java.io.IOException;
import java.util.Random;

import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.util.ArrayList;

import java.util.StringTokenizer;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;


//simple random sampling

public class SRSMapper extends Mapper<Object, Text, NullWritable, Text> {

	private Random rands = new Random();
	private Double percentage;
	private ArrayList<double> scales = new ArrayList<double>(); 

	protected void setup(Context context) throws IOException,
			InterruptedException {
		String strPercentage = context.getConfiguration().get(
				"filter_percentage");
		percentage = Double.parseDouble(strPercentage) / 100.0;
	}

	public void map(Object key, Text value, Context context)
			throws IOException, InterruptedException {
				long count = 0;
				StringTokenizer itr = new StringTokenizer(value.toString(), "\n", false);
	  			while (itr.hasMoreTokens()) {
	  				if (rands.nextDouble() < percentage) {
						String str = itr.nextToken();
	  					String number[] = str.split("\t");
	  					String output = number[2] + "\t" + number[4];
	  					scales.add(Double.parseDouble(number[4]));
	  					++count;
	  				}
	  			}

				Collections.sort(scales);

				double media = 0.0;
				if (count % 2 == 0) {  
            	    media = (scales.get(count / 2 - 1) + scales.get(count / 2)) / 2.0f;  
            	} else {  
            	    media = scales.get(count / 2);  
            	}  

				context.write(NullWritable.get(), media);
	}
}
