# 🚨 Exploring Digital Control in Guitar Pedal Circuits: A Case Study on Digipot and Vactrol Integration

In the world of DIY guitar pedals and audio circuits, finding innovative solutions to achieve precision control without compromising audio quality is always a challenge. Recently, I embarked on an experiment to digitally control a guitar pedal audio circuit, and I wanted to avoid directly using a digital potentiometer (digipot) in the audio path. This led me to explore combining a digipot with a vactrol, a pairing that yielded promising results. Here’s a breakdown of the approach, challenges, and outcomes from this experiment.

## The Challenge: Controlling Resistance Without Noise

In many guitar pedal circuits, altering resistance directly affects the sound. However, if you're using a digipot to control resistance values within an audio circuit, it can introduce "zipper noise" — an undesirable digital artifact that occurs when resistance values change abruptly. Additionally, most digipots are constrained to operate within the control voltage rails (usually 0 to 5V), which can become problematic when dealing with guitar signals that often swing around ±4.5V.

To avoid this, I opted not to place the digipot directly in the audio path. Instead, I wanted to use it in a control path that wouldn't directly interfere with the signal. This is where the idea of combining a digipot with a vactrol came into play.

## The Solution: Digipot and Vactrol Combination

Vactrols (opto-isolators) are known for their ability to control resistance based on the current flowing through an LED. By adjusting the LED's brightness, you can fine-tune the resistance across the vactrol's photocell without introducing noise into the audio signal path. However, I ran into a challenge: driving the vactrol directly with an Arduino's PWM output didn't provide enough granularity in terms of current steps. This resulted in non-linear and imprecise control over the resistance.

To address this, I added a 100kΩ digipot in series with the vactrol’s LED. The new setup was as follows:

- **PWM signal** from the Arduino controlled the overall voltage.
- The **digipot** acted as a variable resistor, offering fine-tuned control over the current supplied to the vactrol LED.
- This combination provided a two-tiered approach to controlling the vactrol’s resistance: 255 steps from the PWM output and 255 resistance steps from the digipot, yielding a total of 256x256 possible control combinations.

## Experimental Setup

I needed a way to map the relationship between the PWM values, digipot resistance, and the resulting vactrol resistance. To do this, I used a voltmeter setup and ran two nested loops through all 256 possible PWM values and 256 digipot resistance settings. I then measured the corresponding resistance of the vactrol in each case and stored the data in a CSV file.

This generated a 256x256 matrix representing the full range of resistance values the vactrol could achieve. I then wrote a Python script to process this data and generate a **lookup table** that could be used in my Arduino project.

## Generating a Linear Resistance Response

One of the goals was to create a linear response in terms of resistance. Using the CSV data, the Python script analyzed the matrix and picked the right combinations of PWM and digipot values to produce a nearly linear resistance range, from almost 0 ohms up to the desired upper bound (in my case, 1MΩ).

The script ultimately generated a `lookup.hpp` file that I could include in my Arduino project. This file provided a quick reference to the correct input values needed to achieve linear resistance control across the desired range.

## Why Use a Digipot to Control a Vactrol?

At first glance, it may seem counterintuitive to use a digipot to control a vactrol instead of just using the digipot directly in the circuit. However, if your goal is to decouple the audio signal path from the digital control path, this setup provides a robust solution. The vactrol ensures that the digital control signals (PWM and digipot adjustments) don’t interfere with the audio signal, while still providing fine-grained control over the resistance.

## Conclusion

This experiment demonstrated the power of combining a digipot and vactrol to achieve linear resistance control in a digitally controlled guitar pedal circuit. By decoupling the digital control from the audio path, I was able to avoid unwanted noise while still having precise control over resistance values. While the solution may seem unconventional, it proved to be an effective method for maintaining audio integrity in guitar pedals with digital controls.

For anyone looking to experiment with digitally controlled audio circuits, this method offers a practical way to maintain clean audio while leveraging digital precision.
