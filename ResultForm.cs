using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MetroFramework.Forms;

namespace FC_to_Python
{
    public partial class ResultForm : MetroForm
    {
        private String message;
        private bool state;
        public ResultForm(bool state, String message)
        {
            this.state = state;
            this.message = message;
            InitializeComponent();
        }

        private void ResultForm_Load(object sender, EventArgs e)
        {
            if (state)
            {
                if (File.Exists(message))
                {
                    resultLabel.Text = @"Success";
                    resultLabel.BackColor = Color.Green;
                    saveBtn.Enabled = true;
                    code.Text = File.ReadAllText(message);
                }
                else
                {
                    resultLabel.Text = @"Error";
                    resultLabel.BackColor = Color.Red;
                    saveBtn.Enabled = false;
                }
            }
            else
            {
                resultLabel.Text = message;
                resultLabel.BackColor = Color.Red;
                saveBtn.Enabled = false;
            }
        }

        private void metroButton1_Click(object sender, EventArgs e)
        {
            //Save Code as .py file
            saveFileDialog1.Title = @"Save";
            saveFileDialog1.Filter = @"Python file (*.py)|*.py";
            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                string file = saveFileDialog1.FileName;
                File.WriteAllText(file, code.Text);
                MessageBox.Show(@"Code Saved Successfully!");
            }
        }
    }
}
