using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;

namespace KodiSkinIDEnumerator
{
    public partial class MainForm : Form
    {
        private FileInfo[] fileList = null;
        private List<KodiSkinFile> skinFiles = new List<KodiSkinFile>();

        private static readonly Random randy = new Random();

        public MainForm()
        {
            InitializeComponent();
        }

        #region Menu and Buttons

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void selectInputToolStripMenuItem_Click(object sender, EventArgs e)
        {
            selectInput();
        }

        private void btnBrowse_Click(object sender, EventArgs e)
        {
            selectInput();
        }

        private void btnParse_Click(object sender, EventArgs e)
        {
            if(this.lblSourcePath.Text.Length == 0)
            {
                MessageBox.Show("No XML Source Path selected");
                return;
            }

            btnBrowse.Enabled = false;
            btnParse.Enabled = false;
            this.lblIDCount.Text = "0";

            // Clear any existing shit
            dataGridView1.DataSource = null;
            dataGridView1.Refresh();
            dataGridView2.DataSource = null;
            dataGridView2.Refresh();
            fileList = null;
            skinFiles = new List<KodiSkinFile>();

            // Now let's build a list of all the xml files in the folder
            DirectoryInfo d = new DirectoryInfo(this.lblSourcePath.Text);
            fileList = d.GetFiles("*.xml");

            DataTable dtFileInfo = new DataTable();
            dtFileInfo.Columns.Add("Name");
            dtFileInfo.Columns.Add("IDCount");
            dtFileInfo.Columns.Add("FirstID");
            dtFileInfo.Columns.Add("LastID");

            int idCount = 0;

            foreach (FileInfo thisFile in fileList)
            {
                int fileIDCount = 0;
                KodiSkinFile nextFile = new KodiSkinFile(thisFile.Name);
                nextFile.contents = File.ReadAllText(thisFile.FullName);

                XmlDocument doc = new XmlDocument();
                doc.Load(new StringReader(nextFile.contents));
                XmlNodeList controlList = doc.GetElementsByTagName("control");
                for (int i = 0; i < controlList.Count; i++)
                {
                    string idVal = "";
                    string typeVal = "";
                    try
                    {
                        idVal = controlList[i].Attributes["id"].Value;
                    } catch (NullReferenceException nullException)
                    {
                        NullReferenceException tmp = nullException;
                        // No ID entry on this control. Asshat.
                        // So we skip this one, since we only care about those with IDs
                        continue;
                    }

                    // We set the typeVal inside these block since the range checks decide if
                    // we continue with this entry in the controlList.
                    if (nudMax.Value > 0)
                    {
                        int x = 0;
                        bool idCheck = int.TryParse(idVal, out x);
                        if (idCheck)
                        {
                            if (int.Parse(idVal) >= nudMin.Value && int.Parse(idVal) <= nudMax.Value)
                            {
                                typeVal = controlList[i].Attributes["type"].Value;
                            }
                            else
                            {
                                continue;
                            }
                        }
                        else
                        {
                            // If the ID was a string like $PARAM[id] we always skip those.
                            // Non-Integer ID's we always skip when doing Mix-Max checks
                            continue;
                        }
                    }
                    else
                    {
                        typeVal = controlList[i].Attributes["type"].Value;
                    }

                    bool controlFilter = true;
                    if (lbControlFilter.SelectedItems.Count > 0)
                    {
                        if (lbControlFilter.SelectedItems.Contains(typeVal))
                        {
                            controlFilter = true;
                        }
                        else
                        {
                            controlFilter = false;
                        }
                    }

                    if (controlFilter)
                    {
                        try
                        {
                            nextFile.idlist.Add(idVal, typeVal);
                        }
                        catch (ArgumentException argException)
                        {
                            // Duplicate Key, FUCK. Someone can't pay attention eh? Hence why this tool is handy dandy bullshit
                            lock (randy)
                            {
                                idVal = controlList[i].Attributes["id"].Value + " (" + randy.Next(1, 1000000).ToString() + ")";
                                nextFile.idlist.Add(idVal, typeVal);
                            }
                        }


                        idCount++;
                        fileIDCount++;
                    }
                }
                skinFiles.Add(nextFile);

                if (fileIDCount == 0 && cbFilterNoID.Checked)
                {
                    continue;
                }

                DataRow drFile = dtFileInfo.NewRow();
                drFile["Name"] = nextFile.name;
                drFile["IDCount"] = fileIDCount;
                if (nextFile.idlist.FirstOrDefault().Key == null)
                {
                    drFile["FirstID"] = "";
                    drFile["LastID"] = "";
                }
                else
                {
                    drFile["FirstID"] = nextFile.idlist.FirstOrDefault().Key.ToString();
                    drFile["LastID"] = nextFile.idlist.LastOrDefault().Key.ToString();
                }
                dtFileInfo.Rows.Add(drFile);
            }
            dataGridView1.DataSource = dtFileInfo;
            this.lblIDCount.Text = idCount.ToString();

            btnBrowse.Enabled = true;
            btnParse.Enabled = true;
        }

        #endregion Menu and Buttons

        private void selectInput()
        {
            FolderBrowserDialog dialog = new FolderBrowserDialog();
            dialog.Description = "Select directory containing Skin's XML files";
            dialog.ShowNewFolderButton = false;
            dialog.SelectedPath = Environment.CurrentDirectory;
            if (dialog.ShowDialog() == DialogResult.OK)
            {
                this.lblSourcePath.Text = dialog.SelectedPath;
                Environment.CurrentDirectory = dialog.SelectedPath;
            }
        }

        private void dataGridView1_RowEnter(object sender, DataGridViewCellEventArgs e)
        {
            dataGridView2.DataSource = null;
            dataGridView2.Refresh();

            KodiSkinFile thisFile = null;

            for (int i = 0; i < skinFiles.Count; i++)
            {
                if(skinFiles[i].name == dataGridView1.Rows[e.RowIndex].Cells[0].Value.ToString())
                {
                    thisFile = skinFiles[i];
                    break;
                }
            }

            if(thisFile.idlist.Count == 0)
            {
                return;
            }

            DataTable dtFileInfo = new DataTable();
            dtFileInfo.Columns.Add("ID");
            dtFileInfo.Columns.Add("Control");

            foreach (KeyValuePair<string, string> entry in thisFile.idlist)
            {
                DataRow drFile = dtFileInfo.NewRow();
                drFile["ID"] = entry.Key;
                drFile["Control"] = entry.Value;
                dtFileInfo.Rows.Add(drFile);
            }
            dataGridView2.DataSource = dtFileInfo;
        }

        private void dataGridView1_RowLeave(object sender, DataGridViewCellEventArgs e)
        {
            // Placeholder for now
        }

        private void dataGridView1_CellDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.ColumnIndex == 0)
            {
                Process fileopener = new Process();
                fileopener.StartInfo.FileName = "explorer";
                fileopener.StartInfo.Arguments = "\"" + lblSourcePath.Text + @"\" + dataGridView1.Rows[e.RowIndex].Cells[0].Value.ToString() + "\"";
                fileopener.Start();
            }
        }
    }

    /// <summary>
    /// This is a Dictionary to hold File name, ID details, and file content.
    /// Why store the contents instead of reading once and doing away with it?
    /// Just in case down the road any other features or needs are added that
    /// may require it post-parsing.
    /// </summary>
    [Serializable]
    public class KodiSkinFile
    {
        public string name = "";
        public string idcount = "";
        public string firstid = "";
        public string lastid = "";
        public string contents = "";
        public SortedList<string, string> idlist = new SortedList<string, string>();


        /// <summary>
        /// Default Constructor
        /// </summary>
        public KodiSkinFile()
        {
        }

        /// <summary>
        /// Default Constructor
        /// </summary>
        public KodiSkinFile(String stringName)
        {
            name = stringName;
        }
    }
}
