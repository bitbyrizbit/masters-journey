temperatures = [30,40,50,60]

def daily_temperatures(temperatures):
    output_list = [0]*len(temperatures)
    for i in range(len(temperatures)):
        for j in range(i+1,len(temperatures)):
            if temperatures[j] > temperatures[i]:
                output_list[i] = j - i
                break
    return output_list
print(daily_temperatures(temperatures))