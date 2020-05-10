using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LanguageIDChecker
{
    public partial class MainForm : Form
    {
        public KodiLangFile langFile = null;

        public MainForm()
        {
            InitializeComponent();
        }

        private void selectInputToolStripMenuItem_Click(object sender, EventArgs e)
        {
            selectInput();

        }

        private void btnBrowse_Click(object sender, EventArgs e)
        {
            selectInput();
        }

        private void selectInput()
        {
            FolderBrowserDialog dialog = new FolderBrowserDialog();
            dialog.Description = "Select directory containing Skin's Language folder";
            dialog.ShowNewFolderButton = false;
            dialog.SelectedPath = Environment.CurrentDirectory;
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                this.lblSourcePath.Text = dialog.SelectedPath;
                Environment.CurrentDirectory = dialog.SelectedPath;
            }
        }

        private void btnParse_Click(object sender, EventArgs e)
        {
            if (this.lblSourcePath.Text.Length == 0)
            {
                MessageBox.Show("No Language File selected");
                return;
            }

            btnBrowse.Enabled = false;
            btnParse.Enabled = false;

        }
    }

    /// <summary>
    /// Name: Name of the file
    /// Content: Entire file contents if rapid parsing is needed again
    /// Lowest: Lowest ID used in file
    /// Highest: Highest ID used in file
    /// IDList: List of all IDs used and their message text
    /// Available: Ranges Available and the total count for quick view and realization
    /// </summary>
    [Serializable]
    public class KodiLangFile
    {
        public string name = "";
        public string content = "";
        public int lowest = 0;
        public int highest = 0;
        public List<string, List<string, string>> idList = new List<string, List<string, string>>();
        public List<string, string> available = new List<string, string>();

        /// <summary>
        /// Default Constructor
        /// </summary>
        public KodiLangFile()
        {
        }

        /// <summary>
        /// Default Constructor
        /// </summary>
        public KodiLangFile(String stringName)
        {
            name = stringName;
        }
    }
}
