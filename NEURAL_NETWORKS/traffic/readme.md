# Traffic Neural Network Project

This project take advantage of Neura Networks with Tensorflow to train an AI to identify which traffic sign appears in a photograph

## Experimentation Process:

### Pool size: 
I start with a pool size of 2x2. However, I realice that she I increment the pool size, the process takes less time (10 seconds with 2x2 and 4 seconds with 3x3 pool size). This is why I decided to implement my model with a pool size of 3x3. This experimentation process is with one layer with 168 units. my accuracy with the pool size of 3x3 was 0.923.

### Number of layers:
I start my experimentation process with 1 layer with 168 units and with a dropout of 0.2, my accuracy was of 0.923. Quickly I noticed that implementing another layer with a quantity of units to 344 my accuracy increase to 0.9428!. However, this implementation increased my processing time to almost 6 seconds

Finally, I decide to implement 3 layers with 672, 336 and 168 units, just because I want to know if the accuracy increase with a big quantity of layers and units. However I notice that the the accuracy did not increase in a significant way and the processing time increase to 18 seconds. 

My finall implementation was two hidden layers with 336 and 168 units. It improves the processing time and my acuracy was near to 0.95. 
