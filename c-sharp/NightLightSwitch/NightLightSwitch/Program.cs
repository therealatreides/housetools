using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Win32;
using System.Threading.Tasks;

namespace NightLightSwitch
{
    class Program
    {
        static void Main(string[] args)
        {

            if (args.Length == 0 || args[0].Contains("?"))
            {
                Console.WriteLine("Please use the following commands:");
                Console.WriteLine("NightLightSwitch <on|off>");
                Console.WriteLine(" ");
                return;
            }

            string theHex = "00";

            switch (args[0].ToLower())
            {
                case "on":
                case "true":
                case "1": theHex = "020000001F844F5B3687D50100000000434201001000D00A02C6149789BBDAE5E6E1EA0100"; break;
                case "off":
                case "false":
                case "0": theHex = "02000000BA85D2243687D5010000000043420100D00A02C614B2E8C9A6E2E6E1EA0100"; break;
                default: theHex = "02000000BA85D2243687D5010000000043420100D00A02C614B2E8C9A6E2E6E1EA0100"; break;
            }

            RegistryKey nightLightKey = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\CloudStore\Store\Cache\DefaultAccount\$$windows.data.bluelightreduction.bluelightreductionstate\Current", true);

            if (nightLightKey != null)
            {
                var value = StringToByteArray(theHex);
                nightLightKey.SetValue("Data", value, RegistryValueKind.Binary);
                nightLightKey.Close();
            }
        }

        public static byte[] StringToByteArray(string hex)
        {
            return Enumerable.Range(0, hex.Length)
                             .Where(x => x % 2 == 0)
                             .Select(x => Convert.ToByte(hex.Substring(x, 2), 16))
                             .ToArray();
        }
    }
}
