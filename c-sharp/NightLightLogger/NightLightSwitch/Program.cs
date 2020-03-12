using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Win32;
using System.Threading.Tasks;
using System.Diagnostics;

namespace NightLightSwitch
{
    class Program
    {
        private static readonly ILogger log = new EventLogger();

        static void Main(string[] args)
        {
            // Pull the registry key to check
            RegistryKey nightLightKey = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\DefaultAccount\Current\default$windows.data.bluelightreduction.settings\windows.data.bluelightreduction.settings", true);

            // Save variable as binary compatible in case need to update "backup" key
            byte[] data =  (byte[])nightLightKey.GetValue("Data");
            // String version of variable for comparison and logging to event viewer as needed
            string dataString = BitConverter.ToString(data);

            // Pull instance for backup key, create it if it doesn't exist
            byte[] backup = (byte[])nightLightKey.GetValue("Backup");
            if (backup == null)
            {
                nightLightKey.SetValue("Backup", data, RegistryValueKind.Binary);
                backup = (byte[])nightLightKey.GetValue("Backup");
                log.Debug("Backup Key generated for the first time");
            }
            // String version of variable for comparison and logging to event viewer as needed
            string backupString = BitConverter.ToString(backup);

            // If the strings do not match, a setting was changed or NightLight was enabled/disabled
            if(dataString != backupString)
            {
                string lastChecked = (string)nightLightKey.GetValue("LastChecked");
                string logMsg = "Settings changed since last check." + Environment.NewLine + "Last Checked: " + lastChecked + Environment.NewLine + "Current time is " + DateTime.Now.ToString("h:mm:ss tt");
                log.Debug(logMsg);
                nightLightKey.SetValue("Backup", data, RegistryValueKind.Binary);
            }
            nightLightKey.SetValue("LastChecked", DateTime.Now.ToString("h:mm:ss tt"), RegistryValueKind.String);
        }
    }

    /// <summary>
    /// Interface and logger class from https://stackoverflow.com/questions/1133355/c-sharp-writing-to-the-event-viewer
    /// </summary>
    interface ILogger
    {
        void Debug(string text);

        void Warn(string text);

        void Error(string text);
        void Error(string text, Exception ex);
    }

    class EventLogger : ILogger
    {
        private string eventLogName = "NightLightLogger";

        public EventLogger()
        {
            if (!EventLog.SourceExists(eventLogName))
                EventLog.CreateEventSource(eventLogName, "Application");
        }

        public void Debug(string text)
        {
            EventLog.WriteEntry(eventLogName, text, EventLogEntryType.Information);
        }

        public void Warn(string text)
        {
            EventLog.WriteEntry(eventLogName, text, EventLogEntryType.Warning);
        }

        public void Error(string text)
        {
            EventLog.WriteEntry(eventLogName, text, EventLogEntryType.Error);
        }

        public void Error(string text, Exception ex)
        {
            Error(text);
            Error(ex.StackTrace);
        }
    }
}
