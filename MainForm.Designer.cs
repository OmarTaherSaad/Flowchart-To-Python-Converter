namespace FC_to_Python
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.insertBtn = new MetroFramework.Controls.MetroButton();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.loadingBox = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.loadingBox)).BeginInit();
            this.SuspendLayout();
            // 
            // insertBtn
            // 
            this.insertBtn.Location = new System.Drawing.Point(166, 163);
            this.insertBtn.Name = "insertBtn";
            this.insertBtn.Size = new System.Drawing.Size(155, 63);
            this.insertBtn.Style = MetroFramework.MetroColorStyle.Silver;
            this.insertBtn.TabIndex = 0;
            this.insertBtn.Text = "Insert Flowchart";
            this.insertBtn.Click += new System.EventHandler(this.insertBtn_Click);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            // 
            // loadingBox
            // 
            this.loadingBox.Image = global::FC_to_Python.Properties.Resources.loading;
            this.loadingBox.Location = new System.Drawing.Point(77, 94);
            this.loadingBox.Name = "loadingBox";
            this.loadingBox.Size = new System.Drawing.Size(331, 230);
            this.loadingBox.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.loadingBox.TabIndex = 1;
            this.loadingBox.TabStop = false;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Center;
            this.ClientSize = new System.Drawing.Size(487, 393);
            this.Controls.Add(this.loadingBox);
            this.Controls.Add(this.insertBtn);
            this.Name = "MainForm";
            this.Text = "Flowchart To Python Converter";
            ((System.ComponentModel.ISupportInitialize)(this.loadingBox)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private MetroFramework.Controls.MetroButton insertBtn;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.PictureBox loadingBox;
    }
}

