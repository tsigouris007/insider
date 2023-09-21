import os, sys, json, argparse

def read_field(field_name, obj):
  try:
    field_value = obj[field_name]
  except Exception as e:
    return ""
  return field_value

def get_filename(classMessage):
  try:
    file_name = classMessage.split("(", 1)[0].strip()
  except Exception as e:
    return ""
  return file_name

def total_findings(json_file):
  issues = {'critical': 0, 'high': 0, 'medium': 0, 'weak': 0}
  ignored = {'critical': 0, 'high': 0, 'medium': 0, 'weak': 0}

  weak = []
  medium = []
  high = []
  critical = []

  weak_cnt = 0
  medium_cnt = 0
  high_cnt = 0
  critical_cnt = 0
  total_cnt = 0

  weak_cwe = []
  medium_cwe = []
  high_cwe = []
  critical_cwe = []

  with open(json_file) as json_f:
    data = json.load(json_f)

    # Get counts
    weak_cnt = data["low"]
    medium_cnt = data["medium"]
    high_cnt = data["high"]
    critical_cnt = data["critical"]
    total_cnt = data["total"]

    for vuln in data["vulnerabilities"]:
      # Read each field
      cvss = read_field("cvss", vuln)
      cwe = read_field("cwe", vuln)
      line = read_field("line", vuln)
      vul_class = read_field("class", vuln)
      vul_id = read_field("vul_id", vuln)
      method = read_field("method", vuln)
      col = read_field("column", vuln)
      descr = read_field("description", vuln)
      classMessage = read_field("classMessage", vuln)
      recommend = read_field("recomendation", vuln)
      file_name = get_filename(classMessage)

      # Get severity level and cwe types
      if cvss <= 3.9:
        severity = "low"
        if not cwe in weak_cwe:
          weak_cwe.append(cwe)
      elif cvss <= 6.9:
        severity = "medium"
        if not cwe in medium_cwe:
          medium_cwe.append(cwe)
      elif cvss <= 8.9:
        severity = "high"
        if not cwe in high_cwe:
          high_cwe.append(cwe)
      else:
        severity = "critical"
        if not cwe in critical_cwe:
          critical_cwe.append(cwe)

      # Pack as a structure
      finding = {
        vul_id: {
          "warning_type": cwe,
          "check_name": cwe,
          "message": descr,
          "file": file_name,
          "line": line,
          "col": col,
          "method": method,
          "recommendation": recommend,
          "class": vul_class,
        }
      }

      # Append to each severity level
      if severity == "low":
        weak.append(finding)
      elif severity == "medium":
        medium.append(finding)
      elif severity == "high":
        high.append(finding)
      else:
        critical.append(finding)

  # Build the final result object
  out = {
    "warnings": {
      "critical": critical_cnt,
      "high": high_cnt,
      "medium": medium_cnt,
      "weak": weak_cnt,
      "total": total_cnt
    },
    "ignored_warnings": {
      "critical": 0,
      "high": 0,
      "medium": 0,
      "weak": 0
    },
    "findings": {
      "critical": critical_cwe,
      "high": high_cwe,
      "medium": medium_cwe,
      "weak": weak_cwe
    },
    "fingerprints": {
      "critical": critical,
      "high": high,
      "medium": medium,
      "weak": weak
    }
  }

  return json.dumps(out, indent=2)

def write_outfile(json_obj, out_file):
  f = open(out_file, "w")
  f.write(json_obj)
  f.close()

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('-i', '--input', type=str, required=True, help='The insider input JSON file.')
  parser.add_argument('-o', '--output', type=str, required=False, default="stdout", help='Specify an output file. If left empty prints to stdout.')
  args = parser.parse_args()

  in_file = args.input
  out_file = args.output

  if not os.path.isfile(in_file):
    print("Please specify an existing input JSON file.")
    sys.exit(2)

  results = total_findings(in_file)

  if out_file == "stdout":
    print(results)
  else:
    write_outfile(results, out_file)

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print("Exception occured.", str(e))
    sys.exit(1)
