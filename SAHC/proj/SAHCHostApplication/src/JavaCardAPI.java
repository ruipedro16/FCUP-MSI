import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import com.sun.javacard.apduio.*;


public class JavaCardAPI {
	
    private Apdu apdu;
    private CadClientInterface cad;
    private Socket sock;
    private OutputStream outputStream;
    private InputStream inputStream;

    public JavaCardAPI() {
        apdu = new Apdu();
    }

    public void establishConnectionToSimulator() {
        try {
            sock = new Socket("localhost", 9025);
            outputStream = sock.getOutputStream();
            inputStream = sock.getInputStream();
            cad = CadDevice.getCadClientInstance(CadDevice.PROTOCOL_T1, inputStream, outputStream);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    public void closeConnection() {
        try {
            sock.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void pwrUp() {
        try {
            if (cad != null) {
                cad.powerUp();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void pwrDown() {
        try {
            if (cad != null) {
                cad.powerDown();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setAPDUHeader(byte[] header) {
        if (header.length > 4 || header.length == 0) {
            System.err.println("The maximum size for APDU Header length is 4 bytes.");
        } else {
            //set the APDU header
            apdu.command = header;
            System.out.println("CLA: " + hexConverter(header[0]));
            System.out.println("INS: " + hexConverter(header[1]));
            System.out.println("P1: " + hexConverter(header[2]));
            System.out.println("P2: " + hexConverter(header[3]));
        }
    }

    public void setAPDUDataLength(byte ln) {
        //set the length of the data command
        apdu.Lc = ln;
        System.out.println("Lc: " + hexConverter(ln));
    }

    public void setDataToBeSent(byte[] data) {
        if (data.length != apdu.Lc) {
            System.err.println("Ensure the length of the message corresponds to the APDUs LC");
        } else {
            apdu.dataIn = data;
            for (int dataIndx = 0; dataIndx < data.length; dataIndx++) {
                System.out.println("dataIn" + dataIndx + ": " + hexConverter(data[dataIndx]));
            }

        }
    }

    public void setResponseExpectedLength(byte ln) {
        //expected length of the data in the response APDU
        apdu.Le = ln;
        System.out.println("Le: " + hexConverter(ln));
    }

    public void sendAndReceiveAPDU() {

        try {
            apdu.setDataIn(apdu.dataIn, apdu.Lc);
            cad.exchangeApdu(apdu);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public byte[] decodeResponseData() {

        byte[] dOut = apdu.dataOut;
        for (int dataIndx = 0; dataIndx < dOut.length; dataIndx++) {
            System.out.println("dataOut" + dataIndx + ": " + hexConverter(dOut[dataIndx]));
        }
        return dOut;

    }

    public byte[] decodeResponseStatus() {
        byte[] statByte = apdu.getSw1Sw2();
        System.out.println("SW1: " + hexConverter(statByte[0]));
        System.out.println("SW2: " + hexConverter(statByte[1]));
        return statByte;
    }


    public String hexConverter(byte byteToConvert) {
        char hex[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
        String str2 = "";
        int num = byteToConvert & 0xff;
        int rem;
        while (num > 0) {
            rem = num % 16;
            str2 = hex[rem] + str2;
            num = num / 16;
        }
        if (str2 != "") {
            return str2;
        } else {
            return "0";
        }
    }
	
}
