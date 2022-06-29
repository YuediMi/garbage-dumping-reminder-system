<?php
require 'database.php';

class user{
    public $id;
    public $height;
    public $iaqaarray;
    public $time;
    public $iaq;
    
    private function __construct($id, $time, $iaq, $height)
    {
        $this->id = $id;
        $this->time = $time;
        $this->iaq = $iaq;
        $this->height = $height;
    }

    # get height by id
    public static function getHeightById($id){
        global $mysqli;
        $stmt = $mysqli->prepare("SELECT height FROM trashinfo where trashid=? order by time desc LIMIT 1;");
        if(!$stmt){
            printf("Query Prep Failed: %s\n", $mysqli->error);
            exit;
        }
        $stmt->bind_param('s', $id);
        $stmt->execute();
        $stmt->bind_result($height);
        if($stmt->fetch()){
            $stmt->close();
            return $height;
        }
        $stmt->close();
        return null;
    }

    # get iaq array
    public static function getiaqArray($id){
        global $mysqli;
        $stmt = $mysqli->prepare('SELECT trashid, time, iaq, height FROM trashinfo where trashid=? order by time desc LIMIT 10;');
        if(!$stmt){
            printf("Query Prep Failed: %s\n", $mysqli->error);
            exit;
        }
        $stmt->bind_param('s', $id);
        $stmt->execute();
        $stmt->bind_result($id, $time, $iaq, $height);
        $iaqaarray = array();
        while($stmt->fetch()){
            $singleiaq = new static($id, $time, $iaq, $height);
            array_push($iaqaarray, $singleiaq);
        }
        $stmt->close();
        return $iaqaarray;
    }

}
?>