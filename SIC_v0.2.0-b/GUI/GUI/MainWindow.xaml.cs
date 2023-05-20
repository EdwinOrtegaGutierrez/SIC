using System;
using System.Drawing;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Drawing.Imaging;
using AForge.Video;
using AForge.Video.DirectShow;
using System.Net;
using System.IO;

namespace GUI
{
    public partial class MainWindow : Window
    {
        private VideoCaptureDevice device;
        
        private bool _processingFrame = false;
        private readonly FilterInfoCollection devices;

        public MainWindow()
        {
            InitializeComponent();
            devices = new FilterInfoCollection(FilterCategory.VideoInputDevice);
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                device = new VideoCaptureDevice(devices[0].MonikerString);
                device.NewFrame += Device_NewFrame;
                device.Start();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void Device_NewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            // Lock the frame processing to avoid race conditions
            if (_processingFrame) return;
            _processingFrame = true;

            using (var bitmap = (Bitmap)eventArgs.Frame.Clone())
            {
                // Update the image displayed in the UI
                image.Dispatcher.Invoke(() => image.Source = ToBitmapSource(bitmap));
            }

            _processingFrame = false;
        }


        private static BitmapSource ToBitmapSource(Bitmap bitmap)
        {
            var bitmapData = bitmap.LockBits( new Rectangle(0, 0, bitmap.Width, bitmap.Height), ImageLockMode.ReadOnly, bitmap.PixelFormat);

            var bitmapSource = BitmapSource.Create( bitmapData.Width, bitmapData.Height, bitmap.HorizontalResolution, bitmap.VerticalResolution,
                PixelFormats.Bgr24, null, bitmapData.Scan0, bitmapData.Stride * bitmapData.Height, bitmapData.Stride);

            bitmap.UnlockBits(bitmapData);
            return bitmapSource;
        }

        private async void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if (device != null && device.IsRunning)
            {
                device.NewFrame -= Device_NewFrame;
                await Task.Run(() =>
                {
                    device.SignalToStop();
                    device.WaitForStop();
                });
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            Window_Closing(sender, new System.ComponentModel.CancelEventArgs());
            Application.Current.Shutdown();
        }

        private void Border_MouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
            {
                DragMove();
            }
        }

        private async void Scan_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Escaneando...");
            device.Stop();

            string url = "http://127.0.0.1:80/facial_recognition";

            try
            {
                await Task.Run(() =>
                {
                    try
                    {
                        WebRequest request = WebRequest.Create(url);
                        request.Method = "GET";
                        request.ContentType = "application/json";

                        using (WebResponse response = request.GetResponse())
                        using (Stream stream = response.GetResponseStream())
                        using (StreamReader reader = new StreamReader(stream))
                        {
                            string responseBody = reader.ReadToEnd();

                            // Mostrar la respuesta en un hilo de la interfaz de usuario principal
                            Dispatcher.Invoke(() =>
                            {
                                MessageBox.Show(responseBody);
                            });
                        }
                    }
                    catch (WebException ex)
                    {
                        // Mostrar el mensaje de error en un hilo de la interfaz de usuario principal
                        Dispatcher.Invoke(() =>
                        {
                            MessageBox.Show("Error al obtener la respuesta: " + ex.Message);
                        });
                    }
                });
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al ejecutar la solicitud: " + ex.Message);
            }

            device.Start();
        }
    }
}
