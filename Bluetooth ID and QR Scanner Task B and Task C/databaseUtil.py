import MySQLdb
import hashlib, binascii, os

class DatabaseUtil:
    """
    Task B
    
    Written by: Ching Loo
    
    DatabaseUtil class.
    
    This class mainly handles connection to the database.
    """
    HOST = "35.189.29.67"
    USER = "root"
    PASSWORD = "password"
    DATABASE = "IoTAssignment2"
    
    
    def __init__(self, connection = None):
        """
        Constructor
        
        Establishes database connection
        
        Parameters:
			connection: Default is none
		
		Returns:
			None
        """
        
        #Checks if a connection has been made with DB
        if(connection == None):
            
            #If no establish a connection
            connection = MySQLdb.connect(DatabaseUtil.HOST, DatabaseUtil.USER,
                DatabaseUtil.PASSWORD, DatabaseUtil.DATABASE)
        self.connection = connection
        
    def close(self):
        """
        Function to close the database connection
        """
        self.connection.close()
        
    
    def getDeviceID(self, vehicleModel):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT engineerDeviceID FROM maintenance WHERE vehicleModel = (%s)", [(vehicleModel)])
            results = cursor.fetchall()
            deviceID=""
            for i in results:
                deviceID=i[0]
            return deviceID
