import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
	private static boolean verifiedPin = false;
	static Menu menu;
	static JavaCardAPI communicator;

	final static byte PASSMNGR_CLA = (byte) 0xB0;
	final static byte VERIFY = (byte) 0x20;
	final static byte GENPASS = (byte) 0x30;
	final static byte GETPASS = (byte) 0x40;
	final static byte RESET = (byte) 0x50;

	final static byte SW1_SUCCESS = (byte) 0x01;
	final static byte SW2_SUCCESS = (byte) 0x00;

	public static void main(String[] args) {
		communicator = new JavaCardAPI();

		// boolean successfulSelection = connectAndSelect();
		// if(successfulSelection){
		// System.out.println("Couldn't select the correct applet!");
		// return;
		// }

		menu = new Menu("Password Manager Menu",
				new String[] { "VERIFY PIN", "GEN PASSWORD", "GET PASSWORD", "RESET PIN" });

		menu.setHandler(1, () -> option1handler(1));

		menu.setHandler(2, () -> option2handler(2));

		menu.setHandler(3, () -> option3handler(3));

		menu.run();
	}

	private static boolean connectAndSelect() {
		byte lengthDataField = 6;
		byte maxDataBytesExpected = 0;
		byte firstParam = 0x04;
		byte secondParam = 0;
		// establishes the socket
		communicator.establishConnectionToSimulator();
		communicator.pwrUp();
		// SELECTING THE PASSWORD MANAGER JAVA APPLET
		byte[] commandHeader = { (byte) 0x00, (byte) 0xA4, firstParam, secondParam };
		communicator.setAPDUHeader(commandHeader);
		communicator.setAPDUDataLength(lengthDataField);
		// SET THIS UP WITH THE AID OF JAVA APPLET
		byte[] data = { (byte) 0x7C, (byte) 0x0F, (byte) 0x1B, (byte) 0x01, (byte) 0x88, (byte) 0x01 };
		communicator.setDataToBeSent(data);
		communicator.setResponseExpectedLength((byte) 0);
		communicator.sendAndReceiveAPDU();
		// Ensure the status of the message is good
		byte[] statusArray = communicator.decodeResponseStatus();
		boolean validation = !(statusArray[0] == SW1_SUCCESS && statusArray[1] == SW2_SUCCESS);
		return validation;
	}

	private static boolean apduVerifyHandler(byte[] pin) {

		byte lengthDataField = 4;
		byte maxDataBytesExpected = 0;
		byte instParamtr1 = 0;
		byte instParamtr2 = 0;

		byte[] commandHeader = { PASSMNGR_CLA, VERIFY, instParamtr1, instParamtr2 };
		communicator.setAPDUHeader(commandHeader);
		communicator.setAPDUDataLength(lengthDataField);

		communicator.setDataToBeSent(pin);
		communicator.setResponseExpectedLength(maxDataBytesExpected);

		communicator.sendAndReceiveAPDU();
		byte[] statusArray = communicator.decodeResponseStatus();

		boolean validation = !(statusArray[0] == SW1_SUCCESS && statusArray[1] == SW2_SUCCESS);
		return validation;
	}

	private static boolean apduGenerateHandler(byte[] identifier) {

		byte lengthDataField = 16;
		byte maxDataBytesExpected = 0;
		byte instParamtr1 = 0;
		byte instParamtr2 = 0;

		byte[] commandHeader = { PASSMNGR_CLA, GENPASS, instParamtr1, instParamtr2 };
		communicator.setAPDUHeader(commandHeader);
		communicator.setAPDUDataLength(lengthDataField);

		communicator.setDataToBeSent(identifier);
		communicator.setResponseExpectedLength(maxDataBytesExpected);

		communicator.sendAndReceiveAPDU();
		byte[] statusArray = communicator.decodeResponseStatus();

		// add status verification

		byte[] dataBuffer = communicator.decodeResponseData();

		String encryptedPwd = new String(dataBuffer);

		boolean dataBaseAPIResponse = savePasswordThroughDatabase(new String(identifier), encryptedPwd);
		return dataBaseAPIResponse;
	}

	private static boolean savePasswordThroughDatabase(String pwID, String encryptedPwd) {
		Connection conn;
		try {
			conn = DriverManager.getConnection(
					"jdbc:mysql://sahc-database.cnjn7q1cet4t.eu-west-1.rds.amazonaws.com:3306", "masterUser",
					"tji41MAc2MPU9zkW4F7m");
			conn.setAutoCommit(false);
			String sqlInsert = "INSERT INTO sys.Passwords VALUES (?,?)";
			PreparedStatement stmt = conn.prepareStatement(sqlInsert);
			stmt.setString(1, pwID);
			stmt.setString(2, encryptedPwd);
			stmt.execute();
			int rowsAffected = stmt.getUpdateCount();
			if (rowsAffected == 0)
				return false;
			conn.commit();
			conn.close();
			return true;
		} catch (SQLException e) {
			System.out.println("Something went wrong during database connection");
			e.printStackTrace();
		}
		return false;

	}

	private static String apduGetHandler(byte[] encPasswordAsBytes) {

		byte lengthDataField = (byte) encPasswordAsBytes.length;
		byte maxDataBytesExpected = 60;
		byte instParamtr1 = 0;
		byte instParamtr2 = 0;

		byte[] commandHeader = { PASSMNGR_CLA, GETPASS, instParamtr1, instParamtr2 };
		communicator.setAPDUHeader(commandHeader);
		communicator.setAPDUDataLength(lengthDataField);

		communicator.setDataToBeSent(encPasswordAsBytes);
		communicator.setResponseExpectedLength(maxDataBytesExpected);

		communicator.sendAndReceiveAPDU();
		byte[] statusArray = communicator.decodeResponseStatus();

		// add status verification

		byte[] passwordAsBytes = communicator.decodeResponseData();

		return new String(passwordAsBytes);

	}

	public static void option1handler(int i) {
		final Scanner sc = new Scanner(System.in);
		System.out.println("Please insert your pin:");
		int pin = sc.nextInt();
		sc.close();
		String pinString = Integer.toString(pin);
		byte[] pinBytes = pinString.getBytes();
		toHexFromBytes(pinBytes);
		verifiedPin = apduVerifyHandler(pinBytes);
		if (!verifiedPin) {
			System.out.println("The PIN was incorrect. Please try again.");
			menu.run();
			return;
		} else {
			System.out.println("The PIN was correct. You can now perform other operations.");
			menu.run();
			return;
		}
	}

	public static void option2handler(int i) {
		if (!verifiedPin) {
			System.out.println("Please insert your pin before trying these operations.");
			menu.run();
			return;
		} else {
			final Scanner sc = new Scanner(System.in);
			boolean validId = false;
			String pwId = "";
			while (!validId) {
				System.out.println("To generate a password, please insert an Identifier(16 chars max): ");
				pwId = sc.next();
				if (pwId.length() <= 16 && pwId.length() > 0)
					validId = true;
			}
			boolean passwordGeneratedSuccessfully = apduGenerateHandler(pwId.getBytes());
			if (!passwordGeneratedSuccessfully) {
				System.out.println("Something went wrong during password generation.");
			} else {
				System.out.println("Password was successfully stored.");
			}
			menu.run();
		}
	}

	public static void option3handler(int i) {
		if (!verifiedPin) {
			System.out.println("Please insert your pin before trying these operations.");
			menu.run();
			return;
		} else {
			final Scanner sc = new Scanner(System.in);
			ArrayList<String> listOfIds = new ArrayList<>();
			listOfIds = fetchIdsFromDatabase();
			if (listOfIds.size() <= 0) {
				System.out.println("You don't have any passwords to show.");
				menu.run();
				return;
			}
			boolean validId = false;
			int option = 0;
			while (!validId) {
				for (int j = 0; j < listOfIds.size(); j++) {
					System.out.println((j + 1) + ": " + listOfIds.get(j));
				}
				System.out.println("Please choose the password identifier you wish to fetch: ");
				option = sc.nextInt();
				if (option > 0 || option < listOfIds.size())
					validId = true;
			}
			String idToFetch = listOfIds.get(option - 1);
			String passwordEncrypted = fetchPasswordById(idToFetch);
			String passwordClearText = apduGetHandler(passwordEncrypted.getBytes());

			if (passwordClearText != null && !passwordClearText.isEmpty()) {
				System.out.println("The password you are looking for is: " + passwordClearText);
			} else {
				System.out.println("Something went wrong decrypting the password.");
			}

		}

	}

	private static ArrayList<String> fetchIdsFromDatabase() {
		Connection conn;
		try {
			conn = DriverManager.getConnection(
					"jdbc:mysql://sahc-database.cnjn7q1cet4t.eu-west-1.rds.amazonaws.com:3306", "masterUser",
					"tji41MAc2MPU9zkW4F7m");
			String sqlInsert = "SELECT idPasswords FROM sys.Passwords";
			PreparedStatement stmt = conn.prepareStatement(sqlInsert);
			boolean gotResults = stmt.execute();
			if (!gotResults)
				return new ArrayList<String>();
			ResultSet listOfIds = stmt.getResultSet();
			ArrayList<String> listOfIdsArray = new ArrayList<>();
			while (listOfIds.next()) {
				listOfIdsArray.add(listOfIds.getString("idPasswords"));
			}
			conn.close();
			return listOfIdsArray;
		} catch (SQLException e) {
			System.out.println("Something went wrong during database connection");
			e.printStackTrace();
		}
		return new ArrayList<String>();
	}

	private static String fetchPasswordById(String idToFetch) {
		Connection conn;
		try {
			conn = DriverManager.getConnection(
					"jdbc:mysql://sahc-database.cnjn7q1cet4t.eu-west-1.rds.amazonaws.com:3306", "masterUser",
					"tji41MAc2MPU9zkW4F7m");
			String sqlInsert = "SELECT idPasswords FROM sys.Passwords";
			PreparedStatement stmt = conn.prepareStatement(sqlInsert);
			boolean gotResults = stmt.execute();
			if (!gotResults)
				return null;

			ResultSet listOfIds = stmt.getResultSet();
			conn.close();
			return listOfIds.getString("EncPassword");
		} catch (SQLException e) {
			System.out.println("Something went wrong during database connection");
			e.printStackTrace();
		}
		return null;
	}

	public static void toHexFromBytes(byte[] bytes) {
		StringBuilder sb = new StringBuilder();
		for (byte b : bytes) {
			sb.append(String.format("0x%02X ", b));
		}
		System.out.println(sb.toString());
	}
}
