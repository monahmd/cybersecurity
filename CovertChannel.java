public class CovertChannel {
    
    // Function to send a message through timing covert channel
    public static void sendMessage(String message) {
        System.out.println("Sending message...");
        for (char c : message.toCharArray()) {
            int ascii = (int) c;
            String binary = Integer.toBinaryString(ascii);
            
            // Append leading zeros to make it 8-bit
            while (binary.length() < 8) {
                binary = "0" + binary;
            }
            
            // Transmit each bit of the character
            for (int i = 0; i < binary.length(); i++) {
                char bit = binary.charAt(i);
                
                // If bit is '0', sleep for a shorter duration (e.g., 100ms)
                // If bit is '1', sleep for a longer duration (e.g., 200ms)
                if (bit == '0') {
                    delay(100);
                } else {
                    delay(200);
                }
            }
        }
        // Send termination character
        delay(300);
        System.out.println("Message sent.");
    }
    
    // Function to receive a message through timing covert channel
    public static String receiveMessage() {
        System.out.println("Receiving message...");
        StringBuilder message = new StringBuilder();
        StringBuilder binary = new StringBuilder();
        
        while (true) {
            long startTime = System.currentTimeMillis();
            delay(100); // Wait for a fixed duration
            
            long endTime = System.currentTimeMillis();
            long duration = endTime - startTime;
            
            // If the duration is closer to 200ms, consider it as '1', otherwise '0'
            if (duration > 150) {
                binary.append('1');
            } else {
                binary.append('0');
            }
            
            // Check if we have received a full character (8 bits)
            if (binary.length() == 8) {
                int ascii = Integer.parseInt(binary.toString(), 2);
                char character = (char) ascii;
                
                // Check for end of message
                if (character == '\0') {
                    break;
                }
                
                // Append character to message
                message.append(character);
                binary.setLength(0); // Reset binary string
            }
        }
        System.out.println("Message received.");
        return message.toString();
    }
    
    // Helper function to introduce delays
    private static void delay(long milliseconds) {
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        String message = "Hello, this is a covert message!";
        
        // Sending the message
        sendMessage(message);
        
        // Receiving the message
        String receivedMessage = receiveMessage();
        System.out.println("Received Message: " + receivedMessage);
    }
}
