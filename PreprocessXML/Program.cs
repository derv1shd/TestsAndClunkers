using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace PreprocessXML
{
    class Program
    {
        static void Main(string[] args)
        {
            var stream = new StreamReader("Sample response - Pedidos.xml");
            StringBuilder input = new StringBuilder(stream.ReadToEnd());

            string pattern = @"<Posicion>[0-9]*</Posicion>";

            foreach(Match match in Regex.Matches(input.ToString(), pattern))
            {
                string newTag = match.Value.Replace("Posicion", "Posicion_Id");
                input.Replace(match.Value, newTag);
            }
        }
    }
}
