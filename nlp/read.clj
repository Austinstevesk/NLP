(require '[clojure.string :as str])

(import [java.io File FileReader BufferedReader FileWriter BufferedWriter])

(defn make_reader [file]
  (-> file File. FileReader. BufferedReader.))


(defn read_data [reader]
  (loop [acc []]
    (let [line (.readLine reader)]
      (if (empty? line)
        acc
        (recur (conj acc line))))))


(def features
  (let [reader (make_reader "nlp_code/features.train")
        feats (.readLine reader)]
    (str/split feats #"\s")))


(defn make_feature_vec [features]
  (zipmap features (repeat (count features) 0)))


(def feature_vec (make_feature_vec features))

(defn training_data [ path_name ]
  (let [reader (make_reader path_name)]
    (read_data reader)))


(defn make_feature[train]
  (clojure.core/vals (merge feature_vec (zipmap train (repeat (count train) 1)))))


(defn training_feature_vec [data] 
  (map 
   (fn [x] (make_feature 
            (str/split x #"\s")
            )) 
   data))


(def training (training_feature_vec (training_data "nlp/training")))     


(defn make_writer[file]
  (-> file File. FileWriter. BufferedWriter.))


(defn writes[writer line]
  (.write writer line))


(def writer (make_writer "nlp/training.csv"))


(map #(writes writer (str (str/join "," %) "\n")) training)


(.flush writer)


(.close writer)



  
