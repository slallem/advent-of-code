package org.example

import java.io.File

class Rule() {
    var index: Int = -1
    var value: String = ""
    var variants: MutableList<MutableList<Rule>> = mutableListOf()

//    companion object {
//        fun parse(s: String) : Rule {
//            return Rule()
//        }
//    }
}

val all_rules = mutableMapOf<Int, Rule>()
val all_messages = mutableListOf<String>()

/*
fun is_matching(msg: String, rule: Rule, prefix: String = "") : Int {
    println("testing ${msg} with rule ${rule.index} prefix ${prefix}")
    if (!rule.value.isEmpty()) {
        // "a" or "b"
        if (msg.isEmpty())
            return -1 // no match (message exhausted but unsatisfied rules remaining)
        return if (msg[0].toString() == rule.value)
            1 // character matching
        else
            -1 // no match
    } else {
        // Evaluate possible sequences
        for (variant in rule.variants) {
            var s = msg
            var p = prefix
            var ok = true
            var cnt = 0
            for (r in variant) {
                val m = is_matching(s, r, p)
                if (m < 0) {
                    ok = false
                    break
                }
                cnt += m
                p += s.substring(0, m)
                s = s.substring(m)
                // continue with the rest of the rules in this sequence
            }
            //check if this sequence is ok
            if (ok && msg == "") {
                println("$prefix is ok")
                return cnt
            }
        }
        //fun is_matching(msg: String, rule: Rule) : Int {
    }
    return -1
}

fun declinerSerie(rules: List<Rule>, prefix : String = "") : String {
    if (prefix.length > 10)
        return ""
    var completion = ""
    for (r in rules) {
        completion += r.index.toString()
        completion += decliner(r, prefix + completion)
    }
    println(prefix + completion)
    return prefix
}


fun decliner(poss: MutableList<MutableList<Rule>>, rule: Rule, prefix : String = "", same_counter : Int = 0) : String {
    if (rule.value.isNotEmpty()) {
        return rule.value
    }
    if (same_counter > 5)
        return "*BREAK*"
    // Evaluate possible sequences
    for (variant in rule.variants) {
        poss.aa
        declinerSerie(variant, prefix)
//        var completion = ""
////        completion += "("
////        completion += variant.size.toString()
////        completion += ")"
//        for (r in variant) {
//            completion += r.index.toString()
//            val ctr = if (r.index == rule.index) same_counter+1 else 0
//            completion += decliner(r, prefix + completion, ctr)
//        }
//        //End of case = print word
//        println(prefix + completion)
    }
    return prefix
}
*/


fun decliner(possibilities: MutableList<MutableList<Rule>>, checkWord: String, verbose: Boolean = false) : Boolean {

    if (verbose) {
        println("======================================================================")
        for (serie in possibilities) {
            for (r in serie) {
                print("%d ".format(r.index))
            }
            println()
        }
    }

    while (possibilities.size > 0) {

        val declinaisons = mutableListOf<MutableList<Rule>>()
        for (poss in possibilities) {
            var mode = 0
            var nbval = 0
            var nbsub = 0
            var gauche = ""
            // -------------- Etape préalable à la déclinaison -----------------
            val newSerieL = mutableListOf<Rule>()
            var newSerieVariants = mutableListOf<MutableList<Rule>>()
            val newSerieR = mutableListOf<Rule>()
            for (rule in poss) {
                if (mode == 0) {
                    if (rule.value.isNotEmpty()) {
                        // it's a value, ok
                        newSerieL.add(rule)
                        gauche += rule.value
                        nbval++
                    } else {
                        // it's a sub rule
                        newSerieVariants = rule.variants
                        mode = 1
                        nbsub++
                    }
                } else {
                    // partie droite, on calculera dans une itération ultérieure
                    // en attendant, prendre tout tel quel
                    newSerieR.add(rule)
                }
            }
            // ------------------- Déclinaisons (ou pas) ------------------
            if (nbsub > 0) {
                // Optim inutile de décliner plus loin si le début ne matche pas
                if (gauche.isEmpty() || checkWord.startsWith(gauche)) {
                    // Déclinaisons...
                    for (serie in newSerieVariants) {
                        val newSerie = mutableListOf<Rule>()
                        newSerie.addAll(newSerieL)
                        newSerie.addAll(serie)
                        newSerie.addAll(newSerieR)
                        // Optim et protection boucle infinie : on exclut les sequences plus grandes que le mot
                        if (newSerie.size <= checkWord.length) {
                            declinaisons.add(newSerie)
                        }
                    }
                } else {
                    // Le début du mot recherché ne correspond pas au début de la combinaison
                    //RAF
                }
            } else {
                // Pas à décliner
                // C'est une valeur finie
                var mot = gauche
                if (verbose) {
                    println("Valeur finie: $mot")
                }
                if (checkWord == mot) {
                    //on a trouvé une combinaison qui matche parfaitement le mot recherché
                    return true
                }
            }
        }

        //Filters here ?

        possibilities.clear()
        possibilities.addAll(declinaisons)

        if (verbose) {
            println("----------------------------------------------------------------------")
            for (serie in possibilities) {
                for (r in serie) {
                    print("%d ".format(r.index))
                }
                println()
            }
        }

//        Thread.sleep(3000)

    }
    return false
}

fun eval(mot: String) : Boolean
{
    val possibilities = mutableListOf<MutableList<Rule>>()
    val startRule = all_rules[0]
    for (v in startRule!!.variants) {
        possibilities.add(v)
    }
    return decliner(possibilities, mot)
}


fun main(args: Array<String>) {

    for (i in 0..200) {
        all_rules[i] = Rule().apply { index = i }
    }

    File("day19.txt").forEachLine { line ->
        if (line.contains(':')) {
            val idx = line.split(":")[0].toInt()
            val seqs = line.split(":")[1].trim().split("|")
            if (seqs[0][0] == '"') {
                all_rules[idx]!!.value = seqs[0][1].toString()
            } else {
                for (seq in seqs) {
                    val vs = seq.trim().split(" ")
                    val l = mutableListOf<Rule>()
                    for (v in vs) {
                        l.add(all_rules[v.toInt()]!!)
                    }
                    all_rules[idx]!!.variants.add(l)
                }
//                println(rules[idx]!!.variants)
            }
        } else {
            if (line.isNotBlank()) {
                all_messages.add(line)
            }
        }
    }


    var tot = 0
    for (message in all_messages) {
        val match = eval(message)
        if (match) {
            tot += 1
        }
//        println(String.format("%s %s", match, message))
    }

    println(String.format("Part 1 - Total %d", tot))

    val l8 = mutableListOf<Rule>()
    l8.add(all_rules[42]!!)
    l8.add(all_rules[8]!!)
    all_rules[8]!!.variants.add(l8)

    val l11 = mutableListOf<Rule>()
    l11.add(all_rules[42]!!)
    l11.add(all_rules[11]!!)
    l11.add(all_rules[31]!!)
    all_rules[11]!!.variants.add(l11)


    tot = 0
    for (message in all_messages) {
        val match = eval(message)
        if (match) {
            tot += 1
        }
//        println(String.format("%s %s", match, message))
    }

    println(String.format("Part 2 - Total %d", tot))

}
