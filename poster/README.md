# WWU MATH Senior Project Poster

This is a fork of the Gemini Beamer poster theme. Adapted to suite the needs of WWU. This specific poster is actually about QAPs.

<p align="center">
<a href="https://raw.githubusercontent.com/anishathalye/assets/master/gemini/poster-gemini.pdf">
<img src="https://raw.githubusercontent.com/anishathalye/assets/master/gemini/poster-gemini-small.png">
</a>
</p>

If you're looking for a beamer presentation theme, take a look at [Auriga].

## Dependencies

* A TeX installation that includes [LuaTeX]
    * You also need `latexmk` if you want to use the provided `Makefile`
* LaTeX package dependencies including beamerposter (these usually come with
  your TeX installation, but if not, you can get them from [CTAN])
* [Raleway] and [Lato], which are both available under Open Font License

## Usage

1. Copy the files in this repository (or clone the repository)

1. In `poster.tex`, set up your paper size, column layout, and scale the
   content as necessary

1. Make a copy of `beamercolorthemegemini.sty`, update the `\usecolortheme`
   line in `poster.tex`, and theme the poster to your liking (optional, but
   highly recommended)

1. Run `make` to build your poster