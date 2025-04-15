# PsiSuite

## Setup

See [setup slides](https://docs.google.com/presentation/d/1vOj6ZTN4r01VZx5Is_DnItr3_VA-MSaOXGwRcOl83ho/edit#slide=id.g34ebc441033_0_207).

If you are on Windows, use WSL.


## Usage

```
./mitmproxy/mitmproxy --tcp-hosts '.*' --set http2=false -s psisuite.py
```

Then, press `B` in the pane to open the browser
