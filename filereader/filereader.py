import re

def main():
###FILEREADER v.  0.9
###READABLE FILE MUST BE NAMED BELOW AND BE IN THE SAME WORKING DIRECTORY###

#program starts if this module is run as main
    file_name = 'uno_data.csv'
    all_readings = All_readings()
    reader = Reader(all_readings, file_name)
    text_ui = Text_ui(all_readings, reader)
    text_ui.start_program()
    
class Reading: #class for individual readings and returning their attributes
    
    def __init__(self, year, month, day, time, status, voltage, temperature):
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.status = status
        self.voltage = voltage
        self.temperature = temperature
        
    def get_temperature(self):
        return self.temperature
    
    def get_voltage(self):
        return self.voltage
    
    def get_year(self):
        return self.year
    
    def get_month(self):
        return self.month
    
    def get_day(self):
        return self.day
    
    def get_status(self):
        return self.status
    
    #return reading as a formatted string when a reading is printed
    def __repr__(self):
        return str('Date: ' + str(self.day) + '.' + str(self.month) + '.' + str(self.year) + ', time: ' + str(self.time) + ', voltage: ' + str(self.voltage) + ' V, temperature: ' + str(self.temperature) + ' C, status: ' + str(self.status))
    
class All_readings: #class for storing individual readings in a list
    
    def __init__(self):
        self.all_readings = []
     
    def add_reading(self, Reading):
        self.all_readings.append(Reading)
                    
    def get_all_readings(self):
        return self.all_readings        
             
class Text_ui: #class responsible for displaying everything for the user and receiving user input
    
    def __init__(self, All_readings, Reader):
        self.all_readings = All_readings
        self.reader = Reader
        
    def start_program(self): # this runs the main UI of the program
        self.reader.read_file() # start reading the file in the reader class
        
        print('FileReader v. 0.9')
        print('help - list all commands')
        while True:
            command = input('Enter command: ')
            
            if command == 'quit' or command == 'exit':
                print("Program terminated by user...")
                break
            
            elif command == 'status':
                print(self.reader.get_status())
            
            elif command == 'help':
                print('List of commands:')
                print('print all - displays all readings')
                print('status - display if saving money or detecting motion')
                print('range - choose temperature range to print')
                print('date - choose day to display readings from')
                print('info - print highest, lowest and mean temperature of selected data')
                print('quit/exit - exits the program')
                
            elif command == 'range':
                try:               
                    range_lowest = float(input('Enter lowest temperature to display: '))
                    range_highest = float(input('Enter highest temperature to display: '))
                    
                except ValueError:
                    print('Invalid input - number expected')
                    continue
                               
                result = self.reader.get_range(range_lowest, range_highest)
                                              
                for i in result:
                    print(i)
                     
                if len(result) == 0:    
                    print('No readings in selected range')
                     
                else:
                    print(self.reader.get_info(result))
                    
            elif command == 'date':
                try: 
                    range_day = float(input('Enter day: '))
                    range_month = float(input('Enter month: '))
                    range_year = float(input('Enter year: '))
                    
                except ValueError:
                    print('Invalid input - number expected')
                    continue

                result = self.reader.date_range(range_day, range_month, range_year)
                
                for i in result:
                    print(i)
                    
                if len(result) == 0:    
                    print('No readings on selected date')
                    
                else:
                    print(self.reader.get_info(result))
                
            elif command == 'print all': #if more than 99 readings in the list, ask to proceed
                if self.reader.get_amount(self.all_readings.get_all_readings()) >= 100:
                    command = input('Displaying ' + str(self.reader.get_amount(self.all_readings.get_all_readings())) + ' readings. Continue? (y/n) ')
                    
                    if command == 'y':
                        for i in self.all_readings.get_all_readings():
                            print(i)
                        
                        print(str(self.reader.get_info(self.all_readings.get_all_readings())))
                                               
                    elif command == 'n':
                        continue
                    
                    else:
                        print('Unknown command')
                 
                elif self.reader.get_amount(self.all_readings.get_all_readings()) < 100:
                    for i in self.all_readings.get_all_readings():
                        print(i)
                        
                    print(str(self.reader.get_info(self.all_readings.get_all_readings())))
                                  
            elif command == 'info':        
                print(str(self.reader.get_info(self.all_readings.get_all_readings())))
                
            else:
                print('Unknown command - enter "help" to list all commands')
            
class Reader: #this class handles all the calculations and logic
    
    #creating instance variables
    def __init__(self, All_readings, file_name):
        self.all_readings = All_readings
        self.lines = []
        self.file_name = file_name
    
    #open named file and read it line by line
    #strip whitespaces    
    def read_file(self):
        with open(self.file_name) as file:
            self.lines = file.readlines()
            self.lines = [line.rstrip() for line in open(self.file_name)]
            self.split_reading()
    
    #split every line of text according to specified delimiters
    #save splitted parts to variables        
    def split_reading(self):
        for i in self.lines:
            year,month,day,time,status,second_status,voltage,temperature = re.split('-| |,',i)
            status = status + ' ' + second_status
            self.add_to_all_readings(year, month, day, time, status, voltage, temperature)
    
    #create an object of the class Reading with parameters received from split_reading
    #add this object to the list of object all_readings        
    def add_to_all_readings(self, year, month, day, time, status, voltage, temperature):
        reading = Reading(year, month, day, time, status, voltage, temperature)
        self.all_readings.add_reading(reading)
     
    #return lowest, highest and mean temperature value of readings in a list       
    def get_info(self, reading_list):
        input_list = reading_list
        output = str(self.get_amount(input_list)) + ' readings, Lowest: ' + str(self.get_lowest(input_list)) + ', highest: ' + str(self.get_highest(input_list)) + ', mean: ' + str(self.get_mean(input_list))
        return output    
    
    # return lowest temperature reading in a list                          
    def get_lowest(self, reading_list):
        input_readings = reading_list
        first_reading = reading_list[0].get_temperature()
        lowest = float(first_reading)
        
        for i in input_readings:
            if float(i.get_temperature()) < lowest:
                lowest = float(i.get_temperature())
                 
        return lowest
    
    #return highest temperature reading in a list
    def get_highest(self, reading_list):
        self.input_readings = reading_list
        self.first_reading = reading_list[0].get_temperature()
        self.highest = float(self.first_reading)
        
        for i in self.input_readings:
            if float(i.get_temperature()) > self.highest:
                self.highest = float(i.get_temperature())
                 
        return self.highest
    
    #return mean temperature reading in a list
    def get_mean(self, reading_list):
        input_readings = reading_list
        number = 0
        amount = 0
        
        for i in input_readings:
            amount += float(i.get_temperature())
            number += 1
            
        mean = amount / number
        return round(mean, 2)
    
    #return how many readings are in a list
    def get_amount(self, reading_list):
        input_readings = reading_list
        amount = 0;
        for i in input_readings:
            amount += 1
            
        return amount
    
    #save readings between the user specified lowest and highest temperature from a list to another list and return it        
    def get_range(self, lowest, highest):
        lowest = float(lowest)
        highest = float(highest)
        list_copy = self.all_readings.get_all_readings()
        result = []
       
        for i in list_copy:
            if (float(i.get_temperature()) >= lowest and float(i.get_temperature()) <= highest):
                result.append(i)
   
                        
        return result
    
    #calculate how many readings in a list are detecting motion and how many are not
    #return the values and their percentages
    def get_status(self):
        list_copy = self.all_readings.get_all_readings()
        saving = 0
        motion = 0
              
        for i in list_copy:
            if i.get_status() == 'Saving money':
                saving += 1
            else:
                motion += 1
            
        saving_percent = round(float((saving / (saving + motion)) * 100), 2) 
        motion_percent = round(float((motion / (saving + motion)) * 100), 2)    
        output = 'Saving money: ' + str(saving) + ' (' + str(saving_percent) + ' %), motion detected: ' + str(motion) + ' (' + str(motion_percent) + ' %)'
        return output  
    
    #save readings from user specified day to another list and return it    
    def date_range(self, day, month, year):
        day = int(day)
        month = int(month)
        year = int(year)
        
        list_copy = self.all_readings.get_all_readings()
        result = []
            
        for i in list_copy:
            if int(i.get_day()) == day and int(i.get_month()) == month and int(i.get_year()) == year:
                result.append(i)
            
        return result
                
if __name__ == '__main__':
    main()




