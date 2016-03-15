#!/usr/bin/env ruby


CANDY_API_KEY = 'Bd1QARJ8BD2rAfE9i9igC8IlDR6ywXVG'
JUICER_API_KEY = 'Yk3KFzyVliTamletdhg7FOAqf26vwGeL'

CANDY_HEADERS = {
  'X-Candy-Platform' => 'Desktop',
  'X-Candy-Audience' => 'International',
  'Accept' => 'application/json'
}

CANDY_ENDPOINT = "http://content-api-a127.api.bbci.co.uk/asset/news/"
CATEGORIES = {:en => %w{world uk world/africa world/europe world/asia world/australia world/latin_america world/middle_east world/us_and_canada technology business football},
              :ar => %w{}
}

require 'rest-client'
require 'json'


class Hash
  # Resurively search for something
  def find_key(key)
    accum = []

    self.keys.each do |k|
      accum << self[k] if k == key

      accum += self[k].find_key(key) if self[k].is_a?(Hash) || self[k].is_a?(Array)
    end

    return accum
  end
end

class Array
  # Resurively search for something
  def find_key(key)
    accum = []

    self.each do |a|
      accum += a.find_key(key) if a.is_a?(Hash)
    end

    accum
  end
end




stubs = {}
CATEGORIES.each do |language, cats|

  puts "\n==> LANG: #{language}"
  cats.each do |cat|

    puts "Category: #{cat}"

    endpoint = "#{CANDY_ENDPOINT}#{cat}?api_key=#{CANDY_API_KEY}"
    res = RestClient::Request.execute(method: :get,
                                         url: endpoint,
                                         headers: CANDY_HEADERS)

    res = JSON.parse(res)
    puts " #{res.length} results."

    
    stubs[language] ||= {}
    stubs[language][cats] ||= []
    (res['results'] || []).each do |r|
      stubs[language][cats] += parse_result(r)
    end

    puts "Total for #{language}, #{cats} => #{stubs[language][cats].length}"

  end

end

# rq = Request.new(CANDY_ENDPOINT)

# , {:params => {:id => 50, 'foo' => 'bar'}}




