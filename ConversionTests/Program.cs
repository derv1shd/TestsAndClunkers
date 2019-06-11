using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConversionTests
{
    class Program
    {
        static void Main(string[] args)
        {
            string sourceData = "1.127.969,89";
            CultureInfo culture = new CultureInfo("es-CL", false);
            Double doubleValue;
            if (Double.TryParse(sourceData, NumberStyles.Currency, culture, out doubleValue))
                Console.WriteLine(doubleValue.ToString());
            else
                Console.WriteLine("Error");
        }
    }
}
