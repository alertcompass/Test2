




#!/usr/bin/env python

import sys, getopt, os, errno, json, subprocess, tempfile

def usage():
    print ("""Usage: %s
    Performs onboarding\offboarding to WDATP locally
""" % sys.argv[0])
    pass

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hc', ['help', 'config='])

    for k, v in opts:
        if k == '-h' or k == '--help':
            usage()
            sys.exit(0)

except getopt.GetoptError as e:
    print (e)
    print ('')
    usage()
    sys.exit(2)

try:
    destfile = '/etc/opt/microsoft/mdatp/mdatp_onboard.json'

    if os.geteuid() != 0:
        print('Re-running as sudo (you may be required to enter sudo''s password)')
        os.execvp('sudo', ['sudo', 'python'] + sys.argv)  # final version

    print('Generating %s ...' % destfile)

    cmd = "sudo mkdir -p '%s'" % (os.path.dirname(destfile))
    subprocess.check_call(cmd, shell = True)

    with open(destfile, "w") as json:
        json.write('''{
  "onboardingInfo": "{\\\"body\\\":\\\"{\\\\\\\"previousOrgIds\\\\\\\":[],\\\\\\\"orgId\\\\\\\":\\\\\\\"f334e347-fd29-43e5-876f-721828e7b2fb\\\\\\\",\\\\\\\"geoLocationUrl\\\\\\\":\\\\\\\"https://winatp-gw-neu.microsoft.com/\\\\\\\",\\\\\\\"datacenter\\\\\\\":\\\\\\\"NorthEurope\\\\\\\",\\\\\\\"vortexGeoLocation\\\\\\\":\\\\\\\"EU\\\\\\\",\\\\\\\"version\\\\\\\":\\\\\\\"1.29\\\\\\\"}\\\",\\\"sig\\\":\\\"5WAK9oIV41WrZuBo1Tkd7RPJBYvUTWxD431n5uSrLweZSuzFD0XeZUEjx5EMcCWIbCjAxt1DpVj3nbYtVwQZRiADVpKaPjiGAEMYNR2Crwh/m1HtzCmVyjSLh7qOrcSOZvZ3xam5Ec0GVxfmR+SmJnj+ryuJj7VdPWJ4yDGBzBhCzCyhM9ME/0aIGUs0Jd7PxVbKuz5qmIUqMV/LvgmGDFMM2An3hi2MPoJfcs19tZSnxfMGGwuayt94F92al2/ttBuizTFSXDU9Q3VrHZItmNQNwL3mO3ayRZCC2ay6I2zBD92Ax/jXzZIQh6+/4cdxkFi0SdqGtI82J9eLzFhtcg==\\\",\\\"sha256sig\\\":\\\"931hRkJ1dpKJnlOewVX0k5Gd8Fr1J/vK+GioU9EwqoVjqUVfV16vxPfkcJr7eHAnub+otuizMW5LlYohoqoygBbea1fvAge83T6jQMkasgNDYhI6zVBoMAhVk1ZAHnhDbSthj5K28nP0chIBH4xDK88VPh6MlU6WBtq3fIuAYsn5RqaYBCbcoKKb9A7l7a3LLyMrnnZtYU9GiIWf2rBRtd0mV4khpzzMCjX5Rc2ptnnBK+HjPZdfLYPyrKJSp+wsiix69nWwK5NufSa6FpAi0NFPDwkiJrPiPiW7hF3mJHn5hCzIDloiUt+go3VddI2akD4ooZV6OEn0GuryQhXVWw==\\\",\\\"cert\\\":\\\"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\\\",\\\"chain\\\":[\\\"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\\\"]}"
}''')

    cmd = "logger -p warning Microsoft ATP: succeeded to save json file %s." % (destfile)
    subprocess.check_call(cmd, shell = True)

except Exception as e:
    print(str(e))
    cmd = "logger -p error Microsoft ATP: failed to save json file %s. Exception occured: %s. " % (destfile, str(e))
    subprocess.call(cmd, shell = True)
    sys.exit(1)