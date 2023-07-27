using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class TCPClient : MonoBehaviour
{
    // Server details
    public string serverIP = "127.0.0.1";
    public int serverPort = 5000;

    // TCP client variables
    private TcpClient client;
    private NetworkStream stream;
    private byte[] receiveBuffer = new byte[4096]; // Adjust the buffer size based on your needs

    // Threading variables
    private Thread receiveThread;
    private bool isRunning = false;

    // Events to notify data reception and connection status changes
    public event Action<string> OnDataReceived;
    public event Action<bool> OnConnected;

    private void Start()
    {
        ConnectToServer();
    }

    private void OnDestroy()
    {
        DisconnectFromServer();
    }

    public void ConnectToServer()
    {
        try
        {
            client = new TcpClient();
            client.Connect(IPAddress.Parse(serverIP), serverPort);
            stream = client.GetStream();
            isRunning = true;
            OnConnected?.Invoke(true);

            // Start the receiving thread
            receiveThread = new Thread(ReceiveData);
            receiveThread.Start();
        }
        catch (Exception e)
        {
            Debug.LogError($"Error connecting to server: {e.Message}");
            OnConnected?.Invoke(false);
        }
    }

    public void DisconnectFromServer()
    {
        if (isRunning)
        {
            isRunning = false;

            if (stream != null)
                stream.Close();

            if (client != null)
                client.Close();

            receiveThread?.Join(500); // Wait for the receiving thread to finish for up to 500 milliseconds
            OnConnected?.Invoke(false);
        }
    }

    public void SendData(string message)
    {
        if (!isRunning)
        {
            Debug.LogWarning("TCP client is not connected.");
            return;
        }

        try
        {
            byte[] data = Encoding.UTF8.GetBytes(message);
            stream.Write(data, 0, data.Length);
        }
        catch (Exception e)
        {
            Debug.LogError($"Error sending data: {e.Message}");
            DisconnectFromServer();
        }
    }

    private void ReceiveData()
    {
        while (isRunning)
        {
            try
            {
                int bytesRead = stream.Read(receiveBuffer, 0, receiveBuffer.Length);
                if (bytesRead > 0)
                {
                    string receivedData = Encoding.UTF8.GetString(receiveBuffer, 0, bytesRead);
                    OnDataReceived?.Invoke(receivedData);
                }
            }
            catch (Exception e)
            {
                Debug.LogError($"Error receiving data: {e.Message}");
                DisconnectFromServer();
            }
        }
    }
}
