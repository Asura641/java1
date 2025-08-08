import java.awt.*;
import java.awt.event.*;

public class SimpleAWTForm extends Frame implements ActionListener {

    // Declare components
    Label label;
    TextField textField;
    Button button;

    // Constructor
    SimpleAWTForm() {
        // Set layout and size
        setLayout(null);
        setSize(400, 200);
        setTitle("AWT Example");

        // Initialize components
        label = new Label("Enter your name:");
        label.setBounds(50, 50, 120, 20);

        textField = new TextField();
        textField.setBounds(180, 50, 150, 20);

        button = new Button("Submit");
        button.setBounds(150, 100, 80, 30);
        button.addActionListener(this);

        // Add components
        add(label);
        add(textField);
        add(button);

        // Window closing event
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                dispose();
            }
        });

        // Show the frame
        setVisible(true);
    }

    // Handle button click
    public void actionPerformed(ActionEvent e) {
        String name = textField.getText();
        label.setText("Welcome, " + name + "!");
    }

    // Main method
    public static void main(String[] args) {
        new SimpleAWTForm();
    }
}
