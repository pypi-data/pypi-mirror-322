======================
atsphinx.toybox.stlite
======================

.. note:: Added by v2024.12.1

Overview
========

This it to embed Stlite content into your documents.

Usage
=====

Enable extension
----------------

Add this into your ``conf.py`` of Sphinx.

.. code-block:: python
   :caption: conf.py

   extensions = [
       "atsphinx.toybox.stlite",
   ]

Configuration
-------------

.. confval:: stlite_version
   :type: str
   :default: |default_stlite_version|

   Using Stlite version.

Demo
====

Source
------

.. code-block:: rst

   .. stlite::
      :id: stlite-demo
      :requirements: matplotlib

      import streamlit as st
      import matplotlib.pyplot as plt
      import numpy as np

      size = st.slider("Sample size", 100, 1000)

      arr = np.random.normal(1, 1, size=size)
      fig, ax = plt.subplots()
      ax.hist(arr, bins=20)

      st.pyplot(fig)

Output
------

.. stlite::
   :id: stlite-demo
   :requirements: matplotlib

   import streamlit as st
   import matplotlib.pyplot as plt
   import numpy as np

   size = st.slider("Sample size", 100, 1000)

   arr = np.random.normal(1, 1, size=size)
   fig, ax = plt.subplots()
   ax.hist(arr, bins=20)

   st.pyplot(fig)

Refs
====

* `Stlite website <https://stlite.net/>`_
* `Stlite repository <https://github.com/whitphx/stlite>`_
