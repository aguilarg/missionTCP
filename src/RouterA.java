import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;


public class RouterA {

    public static void main (String[] args) throws IOException{

        int port = 8080;
        int portToConnectTo = 1111;

        ServerSocket serverSocket = new ServerSocket(port);

        try {
            while(true) {
                Socket ClientSocket = serverSocket.accept();


            }
        }
        catch (Exception e){
            System.err.println("Caught IOException: " + e.getMessage());
        }
    }
}
