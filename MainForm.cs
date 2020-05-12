﻿using System;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;
using MetroFramework.Forms;

namespace FC_to_Python
{
    public partial class MainForm : MetroForm
    {
        private String _filename;
        private bool _state;
        private String _message;
        private BackgroundWorker _backgroundWorker;
        public MainForm()
        {
            InitializeComponent();
            loadingBox.Hide();
            openFileDialog1.Title = @"Open Flowchart Image";
            openFileDialog1.Filter =
                @"Image files (*.jpg, *.jpeg, *.jpe, *.jfif, *.png) | *.jpg; *.jpeg; *.jpe; *.jfif; *.png";
        }

        private void insertBtn_Click(object sender, EventArgs e)
        {
            DialogResult result = openFileDialog1.ShowDialog(this);
            if (result == DialogResult.OK)
            {
                _filename = openFileDialog1.FileName;
                loadingBox.Show();


                _backgroundWorker = new BackgroundWorker();
                _backgroundWorker.DoWork += BackgroundWorker1_DoWork;
                _backgroundWorker.RunWorkerCompleted += BackgroundWorker1_RunWorkerCompleted;
                _backgroundWorker.RunWorkerAsync();
            }

        }

        private void BackgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            string result = "";
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = @"E:\INSTALLATIONS\Anaconda3\python.exe";
            start.Arguments = "\"Autoencoder.py\" \"" + _filename+"\"";
            start.UseShellExecute = false;// Do not use OS shell
            start.CreateNoWindow = true; // We don't need new window
            start.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            start.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)
            using (var process = Process.Start(start))
            {
                if (process != null)
                    using (StreamReader reader = process.StandardOutput)
                    {
                        process.StandardError.ReadToEnd();
                        result = reader.ReadToEnd(); // Here is the result of StdOut(for example: print "test")
                    }
            }
            _message = @"An Error occurred";
            _state = false;
            var place = 0;
            using (var reader = new StringReader(result))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (place == 0)
                    {
                        if (line == "Success")
                        {
                            _state = true;
                        }
                        place++;
                    }
                    else
                    {
                        _message = line;
                    }
                }
            }
        }

        private void BackgroundWorker1_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            loadingBox.Hide();
            ResultForm resultForm = new ResultForm(_state, _message);
            resultForm.ShowDialog();
        }
    }
}