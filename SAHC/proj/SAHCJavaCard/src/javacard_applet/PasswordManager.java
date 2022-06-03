package javacard_applet;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.JCSystem;
import javacard.framework.OwnerPIN;
import javacard.framework.Util;
import javacard.security.AESKey;
import javacard.security.CryptoException;
import javacard.security.KeyBuilder;
import javacard.security.MessageDigest;
import javacard.security.RandomData;
import javacardx.crypto.Cipher;

public class PasswordManager extends Applet {
	private static boolean blocked;

	private static OwnerPIN pin;
	private static OwnerPIN puk;
	
	private final short PASSOWRD_LEN = (short) 60;
    final static short SW_VERIFICATION_FAILED = 0x6300;


	/*
	 * Default PIN: 1234
	 */
	private byte[] DEFAULT_PIN = { (byte) 0x31, (byte) 0x32, (byte) 0x33, (byte) 0x34 };
	private static final byte MAX_PIN_TRIES = (byte) 3;
	private static final byte PIN_SIZE = (byte) 4;
	
	/*
	 * Default PUK: 123456
	 */
	private byte[] DEFAULT_PUK = { (byte) 0x31, (byte) 0x32, (byte) 0x33, (byte) 0x34, (byte) 0x35,
			(byte) 0x36 };
	private static final byte MAX_PUK_TRIES = (byte) 6;
	private static final byte PUK_SIZE = (byte) 6;

	private static final byte AES_KEY_LEN = (byte) 16; // 16 bytes = 128 bits
	private static AESKey masterKey;
	private byte masterKeyBytes[];

	private Cipher cipher; // to encrypt the passwords

	private MessageDigest hash;

	private RandomData rng; // to generate random passwords
	
	/*
	 * Messages
	 */
	private final byte[] CORRECT_PIN_MSG = { (byte) 'C', (byte) 'O', (byte) 'R', (byte) 'R', (byte) 'E', (byte) 'C', (byte) 'T', (byte) ' ', (byte) 'P', (byte) 'I', (byte) 'N' };
	private final byte[] INCORRECT_PIN_MSG = { (byte) 'I', (byte) 'N', (byte) 'C', (byte) 'O', (byte) 'R', (byte) 'R', (byte) 'E', (byte) 'C', (byte) 'T', (byte) ' ', (byte) 'P', (byte) 'I', (byte) 'N' };
	private final byte[] BLOCKED_PIN_MSG = { (byte) 'P', (byte) 'I', (byte) 'N', (byte) ' ', (byte) 'I', (byte) 'S', (byte) ' ', (byte) 'B', (byte) 'L', (byte) 'O', (byte) 'C', (byte) 'k', (byte) 'E', (byte) 'D' };
	private final byte[] VALIDATE_PIN_MSG = { (byte) 'I', (byte) 'N', (byte) 'S', (byte) 'E', (byte) 'R', (byte) 'T', (byte) ' ', (byte) 'P', (byte) 'I', (byte) 'N' };
	private final byte[] TEST_PASSWORD = { (byte) 'P', (byte) 'A', (byte) 'S', (byte) 'S' };
	private final byte[] TEST_READ = { (byte) 'R', (byte) 'E', (byte) 'A', (byte) 'D' };

	private static final short SW_PIN_FAILED = (short) 0x63C0;

	/*
	 * CLA words
	 */
	private static final byte CLA_COMMAND = (byte) 0x80;

	/*
	 * Instruction Words
	 */
	private static final byte INS_CHECKPIN = (byte) 0x0D;
	private static final byte INS_UPDATE_PIN = (byte) 0x05;
	private static final byte INS_PIN_TRIES = (byte) 0x06;
	private static final byte INS_UNBLOCK_PIN = (byte) 0x0A;
	private static final byte INS_GENERATE_PASSWORD = (byte) 0x0B;
	private static final byte INS_READ_PASSWORD = (byte) 0x0C;

	/*
	 * Private constructor that initializes the object's state
	 * 
	 * Allocates all objects needed during the applet's lifetime
	 */
	@SuppressWarnings("deprecation")
	protected PasswordManager() {
		blocked = false;
		
		register();
		
		pin = new OwnerPIN(MAX_PIN_TRIES, PIN_SIZE);
		pin.update(DEFAULT_PIN, (short) 0, (byte) 4);

		puk = new OwnerPIN(MAX_PUK_TRIES, PUK_SIZE);
		puk.update(DEFAULT_PUK, (short) 0, (byte) 6);

		masterKey = (AESKey) KeyBuilder.buildKey(KeyBuilder.TYPE_AES, KeyBuilder.LENGTH_AES_128, false);
		masterKeyBytes = JCSystem.makeTransientByteArray((short) 16, JCSystem.CLEAR_ON_DESELECT);
		
		cipher = Cipher.getInstance(Cipher.ALG_AES_BLOCK_128_CBC_NOPAD, false);
		hash = MessageDigest.getInstance(MessageDigest.ALG_SHA_256, false);
		rng = RandomData.getInstance(RandomData.ALG_PSEUDO_RANDOM);
		
		rng.generateData(masterKeyBytes, (short) 0, (short) 16);
		masterKey.setKey(masterKeyBytes, (short) 0);
		Util.arrayFillNonAtomic(masterKeyBytes, (short) 0, (short) AES_KEY_LEN, (byte) 0);

	}

	public static void install(byte[] bArray, short bOffset, byte bLength) {
		new PasswordManager();//.register(bArray, (short) (bOffset + 1), bArray[bOffset]);
	}

	public boolean select() {
	    if ( pin.getTriesRemaining() == 0 ) return false;
	    return true;
	}
	
	@Override
	public void process(APDU apdu) throws ISOException {
		if (selectingApplet()) {
			return;
		}

		byte[] buffer = apdu.getBuffer();

		if (buffer[ISO7816.OFFSET_CLA] == CLA_COMMAND) {
			switch (buffer[ISO7816.OFFSET_INS]) {
			case INS_CHECKPIN:
				checkPin(apdu);
				break;
			case INS_UPDATE_PIN:
				updatePin(apdu);
				break;
			case INS_PIN_TRIES:
				pinTries();
				break;
			case INS_GENERATE_PASSWORD:
				generatePassword(apdu);
				break;
			case INS_READ_PASSWORD:
				readPassword(apdu);
				break;
			default:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
			}
		}
	}
	
	
	/*
	 * PIN
	 */
	
	private void checkPin(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		
		if(!blocked) {
			if (pin.check(buffer, ISO7816.OFFSET_CDATA, (byte) 4)) {
				short msgLength = (short)CORRECT_PIN_MSG.length;
				Util.arrayCopyNonAtomic(CORRECT_PIN_MSG, (short)0, buffer, (short)0, msgLength);
				apdu.setOutgoingAndSend((short)0, msgLength);
			}
			else {
				ISOException.throwIt(SW_VERIFICATION_FAILED);
			}
		}
		else {
			sendMessage(apdu, BLOCKED_PIN_MSG);
		}
	}
	
	private void incorrectPin(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		
		short msgLength = (short) INCORRECT_PIN_MSG.length;
		Util.arrayCopyNonAtomic(INCORRECT_PIN_MSG, (short) 0, buffer, (short) 0, msgLength);
		apdu.setOutgoingAndSend((short) 0, msgLength);
		
		if (pin.getTriesRemaining() == 0) { // If the limit is exhausted, the applet is blocked
			blocked = true;
			sendMessage(apdu, BLOCKED_PIN_MSG);
		}
	}
	
	private void updatePin(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		
		if (pin.isValidated() && !blocked) {
			byte byteRead = (byte) (apdu.setIncomingAndReceive());
			if (byteRead == 0x04) {
				pin.update(buffer, ISO7816.OFFSET_CDATA, (byte) 4);
				return;
			} else {
				ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);
			}
		} else {
			ISOException.throwIt(ISO7816.SW_COMMAND_NOT_ALLOWED);
		}
	}
	
	private void sendMessage(APDU apdu, byte[] msg) {
		byte[] buffer = apdu.getBuffer();

		short msgLength = (short) msg.length;
		Util.arrayCopyNonAtomic(msg, (short) 0, buffer, (short) 0, msgLength);
		apdu.setOutgoingAndSend((short) 0, msgLength);
	}
	
	private void pinTries() {
		short tries = pin.getTriesRemaining();
		ISOException.throwIt((short) (SW_PIN_FAILED + tries));
	}

	
	/*
	 * Master Key
	 */
	@SuppressWarnings("deprecation")
	private void generateMasterKey() {
			rng.generateData(masterKeyBytes, (short) 0, (short) 16);
			masterKey.setKey(masterKeyBytes, (short) 0);
			Util.arrayFillNonAtomic(masterKeyBytes, (short) 0, (short) AES_KEY_LEN, (byte) 0);
	}
	
	
	/*
	 * Passwords
	 */
	@SuppressWarnings("deprecation")
	private void generatePassword(APDU apdu) {
		try {
			if (pin.isValidated() && !blocked) {
				byte[] buffer = apdu.getBuffer();
//		        buffer[0] = (byte) 0x1;
//				// generate random bytes
				short length = 16;
				byte[] randomBytes = new byte[16];
		        generateSeed(randomBytes, (short) (KeyBuilder.LENGTH_DES3_2KEY / 8));
//				
//				// encrypt
		        cipher.init(masterKey, Cipher.MODE_ENCRYPT);
		        short cipherLength = cipher.update(randomBytes, (short)0, length, buffer, (short) 0);

//		        // output
//				Util.arrayCopyNonAtomic(cipherPass, (short) 0, buffer, (short) 0, length);
		        apdu.setOutgoingAndSend((short) 0, cipherLength);
				
		        
			} else if(blocked) {
				sendMessage(apdu, BLOCKED_PIN_MSG);
			} else {
				sendMessage(apdu, VALIDATE_PIN_MSG);
			}
		}catch (CryptoException e) {
			ISOException.throwIt((short) (0xDDDD));
		} catch(ArrayIndexOutOfBoundsException e) {
			ISOException.throwIt((short) (0xAAAA));
		}
	}
	
	private void readPassword(APDU apdu) {
		if (pin.isValidated() && !blocked) {
			byte[] buffer = apdu.getBuffer();
			short length = 16;
			byte[] unencryptedBufer = new byte[16];
			// decrypt
	        cipher.init(masterKey, Cipher.MODE_DECRYPT);
	        short cipherLength = cipher.update(buffer, (short) ISO7816.OFFSET_CDATA, length, unencryptedBufer, (short) 0);
			
	        // output
			Util.arrayCopyNonAtomic(unencryptedBufer, (short) 0, buffer, (short) 0, length);
	        apdu.setOutgoingAndSend((short) 0, cipherLength);
		} else if(blocked) {
			sendMessage(apdu, BLOCKED_PIN_MSG);
		} else {
			sendMessage(apdu, VALIDATE_PIN_MSG);
		}
	}
	
	   @SuppressWarnings("deprecation")
	private void generateSeed(byte[] randomBytes, short dataSize) {
	        rng.generateData(randomBytes, (byte) 0, dataSize);
	    }
}