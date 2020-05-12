namespace FC_to_Python
{
    partial class ResultForm
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
            this.code = new System.Windows.Forms.RichTextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.resultLabel = new System.Windows.Forms.Label();
            this.saveBtn = new MetroFramework.Controls.MetroButton();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.SuspendLayout();
            // 
            // code
            // 
            this.code.BackColor = System.Drawing.SystemColors.MenuText;
            this.code.ForeColor = System.Drawing.SystemColors.Window;
            this.code.Location = new System.Drawing.Point(23, 151);
            this.code.Name = "code";
            this.code.Size = new System.Drawing.Size(665, 512);
            this.code.TabIndex = 0;
            this.code.Text = "";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Tahoma", 15F);
            this.label1.Location = new System.Drawing.Point(18, 85);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(90, 30);
            this.label1.TabIndex = 2;
            this.label1.Text = "Result:";
            // 
            // resultLabel
            // 
            this.resultLabel.AutoSize = true;
            this.resultLabel.BackColor = System.Drawing.Color.Red;
            this.resultLabel.Font = new System.Drawing.Font("Tahoma", 15F);
            this.resultLabel.ForeColor = System.Drawing.Color.White;
            this.resultLabel.Location = new System.Drawing.Point(131, 85);
            this.resultLabel.Name = "resultLabel";
            this.resultLabel.Size = new System.Drawing.Size(141, 30);
            this.resultLabel.TabIndex = 2;
            this.resultLabel.Text = "Placeholder";
            // 
            // saveBtn
            // 
            this.saveBtn.Location = new System.Drawing.Point(568, 669);
            this.saveBtn.Name = "saveBtn";
            this.saveBtn.Size = new System.Drawing.Size(120, 39);
            this.saveBtn.TabIndex = 3;
            this.saveBtn.Text = "Save Code";
            this.saveBtn.Click += new System.EventHandler(this.metroButton1_Click);
            // 
            // ResultForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(711, 730);
            this.Controls.Add(this.saveBtn);
            this.Controls.Add(this.resultLabel);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.code);
            this.Name = "ResultForm";
            this.Text = "Flowchart To Python Converter";
            this.Load += new System.EventHandler(this.ResultForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.RichTextBox code;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label resultLabel;
        private MetroFramework.Controls.MetroButton saveBtn;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
    }
}