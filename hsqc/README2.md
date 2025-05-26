# 🧪 NMR Data Processing Tutorial

## **Part 2: Phasing with `nmrDraw`**

In this part, we’ll **phase your 1D slice** of the spectrum to make sure peaks are clean, positive, and absorptive — just like in published NMR spectra!

## Step 1: Adjust the Display

Open your spectrum if not already open:

```bash
nd
```

In `nmrDraw`:

1. Use the `+` or `-` buttons to adjust the contour level:

   * This helps hide noise and show only clear peaks.
2. After clicking `+` or `-`, **press the `r` key** to redraw the spectrum.

   * Make sure your **mouse pointer is inside the spectrum window** — otherwise, `r` won't work!

## Step 2: Take a Horizontal Slice (1D Projection)

1. Press the `h` key on your keyboard.

   * This creates a **horizontal 1D slice** of the 2D spectrum.
2. Click and **drag the slice line up or down** using the **left mouse button**.

   * Try to line it up so that you get **2 or 3 clear peaks** in the 1D projection.
   * Ideally, choose peaks that span **both left and right sides** of the spectrum.

## Step 3: Adjust Zero-Order Phase (p0)

1. Look for the **`p0` slider** — it’s a draggable bar (a "rider" with a rectangle in the middle).
2. Click and **drag it left or right** slowly.

   * Watch the 1D projection update as you move it.
3. Your goal:

✅ All peaks should be **positive**
✅ All peaks should look **clean and absorptive (Lorentzian)**
❌ No peaks should be **negative or distorted**

Once your peaks look clean:

* **Note the `p0` value** displayed at the top of the window.
* This is your **zero-order phase correction**.

## Step 4: Save Your p0 and Exit

1. Close `nmrDraw`.
2. Open your processing script again:

```bash
gedit fid_ft.com
```

3. In the script, locate the section where `p0` is set.

   * There are **two p0 values** — edit the **upper one** (this corresponds to **¹H**).

Replace the old value with your new one and run the script again to apply the new phase.

```bash
./fid_ft.com
```

🎉 Great! Your spectrum is now correctly phased. You can already read in the file into ccpNmr analysis or other software.

It is possible that you also need to adjust `p1` (not only `p1`). That is not yet covered, but can be added later. 

➡️ Ready for **baseline correction, peak picking, or more processing**? 
Let me know if you'd like to continue to Part 3.
