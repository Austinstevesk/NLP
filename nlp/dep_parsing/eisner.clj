(defrecord state [s t d c])

(defn FirstOrder [S n]
  (let [C {}
        Keys [:s :t :d :c]
        update (fn[ ]

    (for [k (range 1, (+ n 1))
          s (range (+ n 1))]
      (let [t (+ s k)]
        (if (<= t n)
          (for [[d c] [[">" 0] ["<" 0] [">" 1] ["<" 1]]]
    
            (swap! C assoc (zipmap Keys (s t d c)) (rand)))
          C)))))



